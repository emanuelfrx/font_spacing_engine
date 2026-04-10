import fontforge
import string

def process_font_spacing_complete(input_path, output_path):
    try:
        font = fontforge.open(input_path)
    except Exception as e:
        print(f"[!] Erro ao abrir {input_path}: {e}")
        return None
        
    print(f"    [*] Limpando variáveis de influência (Kerning/Referências)...")
    
    # 1. Remove todas as tabelas de Kerning e ajustes GPOS (Posicionamento)
    for lookup in font.gpos_lookups:
        font.removeLookup(lookup)
    
    # 2. Transforma glifos compostos em contornos reais (essencial para acentos)
    font.selection.all()
    font.unlinkReferences()
    
    # 3. Reseta os Sidebearings para zero absoluto antes do novo cálculo
    for glyph in font.glyphs():
        glyph.left_side_bearing = 0
        glyph.right_side_bearing = 0

    # --- PARAMETRIZAÇÃO DINÂMICA E GRUPOS ÓPTICOS ---
    em_size = font.em
    
    # Cálculos baseados no EM da fonte para evitar padronização fixa
    sep_base = int(em_size * 0.20)  # 20% do EM
    min_sb = int(em_size * 0.02)    # 2% do EM
    max_sb = int(em_size * 0.15)    # 15% do EM

    print(f"    [*] Aplicando AutoWidth por Afinidade Óptica (EM: {em_size})...")

    # Grupo A: Letras Retas
    font.selection.select("H", "I", "M", "N", "U", "i", "l", "n", "u")
    font.autoWidth(sep_base, min_sb, max_sb)

    # Grupo B: Letras Redondas (Compensação de 15% para curvas)
    font.selection.select("O", "C", "Q", "G", "o", "c", "e", "p", "b")
    font.autoWidth(int(sep_base * 0.85), min_sb, max_sb)

    # Grupo C: Diagonais e Abertas (Compensação de 30%)
    font.selection.select("A", "V", "W", "X", "Y", "v", "w", "x", "y", "T")
    font.autoWidth(int(sep_base * 0.70), min_sb, max_sb)

    # Grupo D: O restante do alfabeto
    font.selection.all()
    glifos_processados = [
        "H", "I", "M", "N", "U", "i", "l", "n", "u", 
        "O", "C", "Q", "G", "o", "c", "e", "p", "b",
        "A", "V", "W", "X", "Y", "v", "w", "x", "y", "T"
    ]
    
    for char in glifos_processados:
        if char in font:
            font.selection.select(("less", None), char)
            
    font.autoWidth(sep_base, min_sb, max_sb)

    # --- EXTRAÇÃO DE DADOS ---
    print(f"    [*] Extraindo métricas matemáticas geradas...")
    caracteres = string.ascii_uppercase + string.ascii_lowercase
    metricas_extraidas = {}

    for char in caracteres:
        suffix_e = f"{char}e"
        suffix_d = f"{char}d"
        
        if char in font:
            # Captura os valores finais arredondados
            metricas_extraidas[suffix_e] = round(font[char].left_side_bearing, 2)
            metricas_extraidas[suffix_d] = round(font[char].right_side_bearing, 2)
        else:
            metricas_extraidas[suffix_e] = 0
            metricas_extraidas[suffix_d] = 0

    font.generate(output_path)
    font.close()
    return metricas_extraidas
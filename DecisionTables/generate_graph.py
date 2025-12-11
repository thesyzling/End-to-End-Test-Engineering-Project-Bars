import pandas as pd
import matplotlib.pyplot as plt

def save_decision_table_image():
    # 1. Veriyi Hazırla (Aynı mantık)
    data = {
        "Rule ID": ["DT-01", "DT-02", "DT-03", "DT-04"],
        "Description": ["Early Morning", "Standard Hours", "Peak Evening", "Invalid Hour"],
        "Input (Hour)": [8, 14, 19, 25],
        "Multiplier": [0.8, 1.0, 1.5, "Error"],
        "Expected Result": ["Discounted", "Base Price", "Increased", "ValueError"]
    }
    df = pd.DataFrame(data)

    # 2. Çizim Alanı Oluştur
    fig, ax = plt.subplots(figsize=(10, 3)) # Genişlik: 10, Yükseklik: 3
    ax.axis('tight')
    ax.axis('off') # X ve Y eksenlerini (çizgileri) gizle

    # 3. Tabloyu Çiz
    # cellText: Tablonun içi, colLabels: Başlıklar, loc: Konum
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')

    # 4. Görselliği Güzelleştir (Opsiyonel)
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 1.5) # Sütun genişliği ve Satır yüksekliği ölçeği

    # Başlık Satırını Renklendir (Gri yapalım)
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor('#40466e') # Koyu mavi/gri başlık
        elif row % 2 == 0:
             cell.set_facecolor('#f2f2f2') # Satırları zebra gibi renklendir

    # 5. Resmi Kaydet
    plt.title("Dynamic Pricing Decision Table", fontweight="bold", pad=20)
    plt.savefig('decision_table.png', bbox_inches='tight', dpi=300)
    
    print("✅ Tablo başarıyla 'decision_table.png' olarak kaydedildi!")

if __name__ == "__main__":
    save_decision_table_image()
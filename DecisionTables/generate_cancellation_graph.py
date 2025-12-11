import pandas as pd
import matplotlib.pyplot as plt

def save_cancellation_table_image():
    # SENARYO:
    # 1. Giriş sayısı 2'den azsa -> %100 İade (Class fark etmez)
    # 2. Giriş sayısı 2 ve üzeriyse -> Class tipine göre değişir (Yoga %50, Boxing %0, Fitness %20 vb.)
    
    data = {
        "Rule ID": ["DT-01", "DT-02", "DT-03", "DT-04", "DT-05", "DT-06", "DT-07", "DT-08", "DT-09", "DT-10", "DT-11", "DT-12", "DT-13"],
        "Condition: Attendance < 2?": ["Yes", "Yes", "No", "Yes", "No","Yes", "No","Yes", "No","Yes", "No","Yes", "No",],
        "Condition: Class Type": ["-", "Yoga", "Yoga","Boxing","Boxing","Fitness","Fitness", "Basketball","Basketball", "Tennis", "Tennis","Swimming","Swimming"],
        "Action: Refund Rate": ["1.0 (%100)", "1.0 (%100)", "0.3 (%30),","1.0(%100)","0.5(%50)","1.0(%100)","0.1(%10)","1.0(%100)","0.4(%40)","1.0(%100)","0.8(%80)","1.0(%100)","0.15(%15)"],
        "Expected Result": ["Full Refund","Full Refund", "Partial Refund","Full Refund", "Partial Refund","Full Refund", "Partial Refund","Full Refund", "Partial Refund","Full Refund", "Partial Refund","Full Refund", "Partial Refund",]
    }
    
    df = pd.DataFrame(data)

    # Çizim Alanı
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axis('tight')
    ax.axis('off')

    # Tabloyu Çiz
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')

    # Görsellik Ayarları
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 1.8)

    # Renklendirme
    for (row, col), cell in table.get_celld().items():
        if row == 0: # Başlık
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor('#8B0000') 
        elif row % 2 == 0:
             cell.set_facecolor('#f9f9f9')

    plt.title("Cancellation & Refund Decision Table", fontweight="bold", pad=10)
    plt.savefig('cancellation_decision_table.png', bbox_inches='tight', dpi=300)
    
    print("✅ Tablo 'cancellation_decision_table.png' olarak kaydedildi!")

if __name__ == "__main__":
    save_cancellation_table_image()
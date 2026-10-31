import awkward as ak
from services.parsing.event_selection import apply_parsing_event_selection

def run_test():
    # 1. יצירת נתוני דמה (Mock Events) הכוללים פוטונים, אלקטרונים, מיונים וסילונים
    mock_events = ak.Array([
        {
            "Electrons": [{"pt": 25.0, "eta": 0.5, "phi": 1.0}],
            "Muons": [],
            "Jets": [{"pt": 50.0, "eta": 0.1, "phi": 0.0}],
            # אירוע 1: שני פוטונים תקינים (pT > 20, מחוץ לסדק ה-ECAL)
            "Photons": [
                {"pt": 30.0, "eta": 0.2, "phi": 1.5},
                {"pt": 40.0, "eta": -0.8, "phi": -1.0}
            ],
        },
        {
            "Electrons": [{"pt": 30.0, "eta": 0.1, "phi": 0.0}],
            "Muons": [{"pt": 35.0, "eta": -0.2, "phi": 0.5}],
            "Jets": [],
            # אירוע 2: פוטון אחד רך מדי (pT=15 < 20) ופוטון אחד בסדק ה-ECAL (eta=1.5) -> שניהם אמורים להיזרק
            "Photons": [
                {"pt": 15.0, "eta": 0.1, "phi": 0.0},
                {"pt": 50.0, "eta": 1.5, "phi": 0.0}
            ],
        }
    ])

    print("=== בדיקת שדות לפני הרצת apply_parsing_event_selection ===")
    print("Events fields:", mock_events.fields)

    # 2. הרצת הצינור
    processed_events = apply_parsing_event_selection(mock_events)

    print("\n=== בדיקת שדות לאחר הרצת הצינור ===")
    print("Processed fields:", processed_events.fields)

    # 3. אימות קיום השדה Photons והחלת הסינונים
    if "Photons" in processed_events.fields:
        print("\nSUCCESS: השדה 'Photons' קיים ונשמר ב-events!")
        
        # הדפסת מספר הפוטונים שעברו את הסינון בכל אירוע
        photon_counts = ak.num(processed_events["Photons"]).tolist()
        print(f"כמות פוטונים שעברו סינון בכל אירוע: {photon_counts}")
        
        # אימות ספירת non-jet fields
        non_jet_fields = [f for f in processed_events.fields if f != "Jets"]
        print(f"השדות שנלכדים בספירת 4 האובייקטים: {non_jet_fields}")
    else:
        print("\nERROR: השדה 'Photons' לא נמצא ב-events.fields!")

if __name__ == "__main__":
    run_test()
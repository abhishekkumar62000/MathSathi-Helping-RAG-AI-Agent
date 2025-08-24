import pandas as pd

def load_jeebench_dataset():
    import json
    with open("data/test.json", "rb") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    # Kuch files mein subject key ho sakta hai, kuch mein nahi, toh safe check lagao
    if "subject" in df.columns:
        df = df[df["subject"].str.lower() == "math"]
    return df[['question', 'gold']]

if __name__ == "__main__":
    load_jeebench_dataset()
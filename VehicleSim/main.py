import requests
import time
import pandas as pd
# import kagglehub


TARGET_URL = "https://tmbd.me/api" 
CSV_FILE = ".\VehicleSim\Test.csv"
DELAY = 0.2

# # Download latest version
# path = kagglehub.dataset_download("meowmeowmeowmeowmeow/gtsrb-german-traffic-sign")

# print("Path to dataset files:", path)


def send_image(file_path):
    """
    Sends an image to the target URL.

    Args:
        file_path (str): Path to the image file.

    Returns:
        response: Server's response object.
    """
    with open(file_path, 'rb') as file:
        files = {'file': file}
        try:
            response = requests.post(TARGET_URL, files=files)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error sending {file_path}: {e}")
            return None

def main():
    
    data = pd.read_csv(CSV_FILE)

    if "Path" not in data.columns or "ClassId" not in data.columns:
        print("Error: CSV must contain 'Path' and 'ClassId' columns.")
        return
    hitCount = 0
    missCount = 0
    for _, row in data.iterrows():
        image_path = row["Path"]
        expected_class = int(row["ClassId"])

        # Send the image to the API
        response = send_image("./VehicleSim/" + image_path)

        if response:
            predicted_class = int(response.json()['class'])

            if predicted_class == expected_class:
                print(f"SUCCESS: {image_path} - Predicted class '{predicted_class}' matches expected '{expected_class}'.")
                hitCount += 1
            else:
                print(f"FAILURE: {image_path} - Predicted class '{predicted_class}' does NOT match expected '{expected_class}'.")
                missCount += 1
            
        # time.sleep(DELAY)
    print(f"Final accuracy: {(hitCount/(hitCount+missCount))*100}% on {hitCount+missCount} attempts.")


if __name__ == "__main__":
    main()

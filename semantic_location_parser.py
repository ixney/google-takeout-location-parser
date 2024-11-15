import os
import csv
import json
import datetime

def process_file(file_path, data_writer):
    print(f"Reading file: {file_path}")
    try:
        with open(file_path, encoding='utf-8-sig') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from file {file_path}: {e}")
                return

            for obj in data['timelineObjects']:
                if 'placeVisit' in obj:
                    try:
                        location = obj.get('placeVisit', {}).get('location', {})
                        name = location.get('name', location.get('address', ''))
                        lat = obj['placeVisit']['location']['latitudeE7'] / 10 ** 7
                        lon = obj['placeVisit']['location']['longitudeE7'] / 10 ** 7
                        timestamp = obj['placeVisit']['duration']['startTimestamp']
                        address = location.get('address', '')
                        placeid = location.get('placeId', '')
                        # Convert the timestamp to a datetime object
                        try:
                            datetime_obj = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
                        except ValueError:
                            datetime_obj = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
                        # Convert the datetime object to Unix epoch time
                        epoch_time = int(datetime_obj.timestamp())
                        # Write the data to the CSV file
                        data_writer.writerow([timestamp, lat, lon, address, placeid, name, epoch_time])
                    except KeyError as e:
                        print(f"Missing key in JSON object: {e}")  # Debugging line
    except FileNotFoundError as e:
        print(f"File not found: {file_path}: {e}")  # Debugging line
    except Exception as e:
        print(f"Unexpected error processing file {file_path}: {e}")  # Debugging line


def main():
    root_dir = r".\Takeout\Location History (Timeline)\Semantic Location History"
    output_file = "semantic_location_history.csv"
    if not os.path.exists(root_dir):
        print(f"Root directory does not exist: {root_dir}")
        return

    try:
        with open(output_file, 'w', newline='') as outfile:
            data_writer = csv.writer(outfile)
            data_writer.writerow(["timestamp", "latitude", "longitude", "address", "placeid", "name", "epoch_time"])
            for subdir, dirs, files in os.walk(root_dir):
                print(f"Checking directory: {subdir}")
                for file in files:
                    if file.endswith(".json"):
                        file_path = os.path.join(subdir, file)
                        print(f"Processing file: {file_path}")
                        process_file(file_path, data_writer)
                    else:
                        print(f"Skipping file: {file}")
        print("semantic_location_history.csv created in current directory")
    except IOError as e:
        print(f"Error opening/writing to CSV file: {e}")
    except Exception as e:
        print(f"Unexpected error in main: {e}")


if __name__ == "__main__":
    main()

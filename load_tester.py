import time
import random
import requests
import os
from concurrent.futures import ThreadPoolExecutor

class ImageClassificationLoadTester:
    def __init__(self, workload, endpoint, image_folder):
        self.workload = workload
        self.endpoint = endpoint
        self.image_folder = image_folder
        print(f"Contents of the image folder ({image_folder}):")
        all_files = os.listdir(image_folder)
        print(all_files)
        self.image_files = [f for f in all_files if f.endswith(('.jpg', '.JPEG', '.png'))]
        print(f"Filtered image files: {self.image_files}")
        print(f"Initialized with {len(self.image_files)} image files.")
        absolute_paths = [os.path.abspath(os.path.join(image_folder, f)) for f in self.image_files]
        print(f"Absolute paths of filtered images: {absolute_paths}")


    def send_request(self):
        if not self.image_files:
            print("No image files found to send.")
            return

        image_file = random.choice(self.image_files)
        image_path = os.path.join(self.image_folder, image_file)
        
        print(f"Sending request with image: {image_file}")
        
        with open(image_path, 'rb') as img:
            files = {'file': (image_file, img, 'image/jpeg')}
            response = requests.post(self.endpoint, files=files)
        
        if response.status_code == 200:
            print(f"Image {image_file} processed successfully. Predictions: {response.json()}")
        else:
            print(f"Error processing image {image_file}. Status code: {response.status_code}")

    def run_workload(self):
        for requests_per_second in self.workload:
            print(f"Sending {requests_per_second} requests per second")
            start_time = time.time()
            with ThreadPoolExecutor(max_workers=requests_per_second) as executor:
                executor.map(lambda _: self.send_request(), range(requests_per_second))
            elapsed_time = time.time() - start_time
            if elapsed_time < 1:
                time.sleep(1 - elapsed_time)

def main():
    workload_file = 'wl.txt'
    if not os.path.exists(workload_file):
        print(f"Workload file {workload_file} not found!")
        return
    
    with open(workload_file, 'r') as f:
        workload = [int(num) for num in f.read().split()]
    
    print(f"Loaded workload: {workload}")
    tester = ImageClassificationLoadTester(
        workload=workload,
        endpoint="http://127.0.0.1:60929/predict",  # Update endpoint
        image_folder=os.path.join("/Users/ammar/Desktop/SS2024/Cloud_Computing/Elastic ML Inference Serving/imagenet-sample-images-master")  # Update image folder path
    )
    
    tester.run_workload()

if __name__ == "__main__":
    main()

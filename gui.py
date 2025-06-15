import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import subprocess
import os
import shutil
import threading

class ShadowRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shadow Detection and Removal")
        self.root.geometry("850x620")
        self.root.configure(bg='white')

        # Title Label
        tk.Label(root, text="Shadow Detection and Removal", font=("Arial", 20), bg="white").pack(pady=10)

        # Image Display Frames
        frame = tk.Frame(root, bg='white')
        frame.pack(pady=10)

        self.input_canvas = tk.Canvas(frame, width=300, height=300, bg='lightgray')
        self.input_canvas.grid(row=0, column=0, padx=20)

        self.output_canvas = tk.Canvas(frame, width=300, height=300, bg='lightgray')
        self.output_canvas.grid(row=0, column=1, padx=20)

        # Button Frame
        button_frame = tk.Frame(root, bg='white')
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Upload Image", command=self.upload_image, width=18).grid(row=0, column=0, padx=8)
        tk.Button(button_frame, text="Remove Shadow", command=self.remove_shadow, width=18).grid(row=0, column=1, padx=8)
        tk.Button(button_frame, text="Reprocess", command=self.reprocess_image, width=18).grid(row=0, column=2, padx=8)
        tk.Button(button_frame, text="Clear", command=self.clear_all, width=18).grid(row=0, column=3, padx=8)

        # Status Label
        self.status_label = tk.Label(root, text="", font=("Arial", 12), bg="white", fg="blue")
        self.status_label.pack()

        # Variables for Image Paths
        self.image_path = ""
        self.input_img_tk = None
        self.output_img_tk = None

    def upload_image(self):
        """Upload an image and display it in the input canvas."""
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if path:
            self.image_path = path
            self.load_and_display_input(path)
            os.makedirs("Input_images", exist_ok=True)
            shutil.copy(path, "Input_images/input.jpg")

    def load_and_display_input(self, path):
        """Display the input image on the input canvas."""
        img = Image.open(path)
        img = ImageOps.fit(img, (300, 300), Image.ANTIALIAS)
        self.input_img_tk = ImageTk.PhotoImage(img)
        self.input_canvas.delete("all")
        self.input_canvas.create_image(0, 0, anchor=tk.NW, image=self.input_img_tk)

    def load_and_display_output(self, path):
        """Display the output image on the output canvas."""
        img = Image.open(path)
        img = ImageOps.fit(img, (300, 300), Image.ANTIALIAS)
        self.output_img_tk = ImageTk.PhotoImage(img)
        self.output_canvas.delete("all")
        self.output_canvas.create_image(0, 0, anchor=tk.NW, image=self.output_img_tk)

    def run_removal_process(self):
        """Run the shadow removal process using the external model."""
        cmd = "python demo.py --model Models/srdplus-pretrained --vgg_19_path ../srdplus-pretrained/imagenet-vgg-verydeep-19.mat --input_dir Input_images --result_dir output_images"
        result = subprocess.run(cmd, shell=True)

        if result.returncode == 0 and os.path.exists("output_images/input.png"):
            self.load_and_display_output("output_images/input.png")
            self.status_label.config(text="Shadow Removed Successfully!", fg="green")
        else:
            self.status_label.config(text="Failed to process image.", fg="red")

    def remove_shadow(self):
        """Perform shadow removal on the uploaded input image."""
        if not os.path.exists("Input_images/input.jpg"):
            messagebox.showwarning("No Image", "Please upload an image first.")
            return

        self.status_label.config(text="Processing...", fg="orange")
        self.root.update()

        # Run shadow removal in background
        threading.Thread(target=self.run_removal_process).start()

    def reprocess_image(self):
        """Reprocess the existing output image (second box) for shadow removal."""
        if not os.path.exists("output_images/input.png"):
            messagebox.showwarning("No Output", "No output image available to reprocess.")
            return

        # Use output image as the new input for reprocessing
        shutil.copy("output_images/input.png", "Input_images/input.jpg")
        
        self.output_canvas.delete("all")
        self.output_img_tk = None
        self.status_label.config(text="Reprocessing...", fg="orange")
        self.root.update()

        # Run shadow removal again on the output image (now treated as input)
        threading.Thread(target=self.run_removal_process).start()

    def clear_all(self):
        """Clear both input and output images and reset the app state."""
        self.input_canvas.delete("all")
        self.output_canvas.delete("all")
        self.status_label.config(text="")
        self.image_path = ""

        # Remove saved images
        if os.path.exists("Input_images/input.jpg"):
            os.remove("Input_images/input.jpg")
        if os.path.exists("output_images/input.png"):
            os.remove("output_images/input.png")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ShadowRemoverApp(root)
    root.mainloop()

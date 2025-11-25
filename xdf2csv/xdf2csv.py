import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
import xml.etree.ElementTree as ET
import pyxdf
import numpy as np

def browse_file():
    # Open file dialog to select an XDF file
    file_path = filedialog.askopenfilename(
        title="Select an XDF File",
        filetypes=[("XDF files", "*.xdf"), ("All files", "*.*")]
    )
    if file_path:
        # Display the selected file path in the textbox
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)


def save_csv_file(stream, filename):
    print(f"\t Saving {filename}.csv")
    
    np.savetxt(filename+'.csv', stream['time_series'], delimiter=',', fmt='%s')

    with open(filename+'.json', 'w') as f:
        json.dump(stream['info'], f, indent=2, cls=NpEncoder)

    print(f"\t Saving timestamps {filename}.csv")
    np.savetxt(filename+'_timestamps.csv', stream['time_stamps'], delimiter=',', fmt='%s')


def convert_file():
    # Get the selected file path from the textbox
    file_path = file_entry.get()
    if not file_path:
        messagebox.showerror("Error", "No file selected!")
        return

    try:
        # Start progress bar
        progress_bar["value"] = 0
        root.update_idletasks()

        # Load the XDF file using pyxdf
        streams, _ = pyxdf.load_xdf(file_path)

        # Update progress bar (50%)
        progress_bar["value"] = 50
        root.update_idletasks()

        print("\n----------------------------------------------------------------------")
        print("----------------------------------------------------------------------")
        print(file_path)

        data, header = pyxdf.load_xdf(xdf_files[file_path])
        for i, stream in enumerate(data):
            # print(h, stream['info']['type'][0])
            if(stream['info']['type'][0] == 'Audio'):
                print(f"{file_path}-Stream {i}: {len(stream['time_series'])} |   Name: {stream['info']}")


        for i, stream in enumerate(streams):
            if(stream['info']['type'][0] == 'Data'):
                csv_file_path = file_path.replace(".xdf", "-"+stream['info']['name']+".xml")
                save_csv_file(stream, csv_file_path)

        # # Create an XML structure
        # root_element = ET.Element("XDFContents")
        # for i, stream in enumerate(streams):

        #     print(f"\nStream {i + 1}:")
        #     print(f"Stream Name: {stream['info']['name']}")
        #     print(f"Channel Count: {stream['info']['channel_count']}")
        #     print(f"Nominal Sampling Rate: {stream['info']['nominal_srate']} Hz")
            
        #     # Print the time series data
        #     print("Time Series Data:")
        #     print(stream['time_series'])

        #     # Print timestamps
        #     print("Timestamps:")
        #     print(stream['time_stamps'])

        #     stream_element = ET.SubElement(root_element, "Stream", id=str(i))
        #     for key, value in stream.items():
        #         child = ET.SubElement(stream_element, key)
        #         child.text = str(value)

        # # Save XML to the same location with the same filename
        # xml_file_path = file_path.replace(".xdf", ".xml")
        # tree = ET.ElementTree(root_element)
        # tree.write(xml_file_path)

        # # Update progress bar (100%)
        # progress_bar["value"] = 100
        # root.update_idletasks()

        # Notify the user of success
        messagebox.showinfo("Success", f"CSV file created: {csv_file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process XDF file: {str(e)}")
    finally:
        # Reset progress bar after completion or failure
        progress_bar["value"] = 0

# Create Tkinter interface
root = tk.Tk()
root.title("XDF to CSV Converter")
root.geometry("500x300")

# Label for instructions
label = tk.Label(root, text="Select an XDF file to convert to CSV", font=("Arial", 12))
label.pack(pady=10)

# Textbox to display selected file path
file_entry = tk.Entry(root, width=50, font=("Arial", 10))
file_entry.pack(pady=10)

# Browse button to select a file
browse_button = tk.Button(root, text="Browse File", command=browse_file, font=("Arial", 12))
browse_button.pack(pady=10)

# Convert button to start conversion process
convert_button = tk.Button(root, text="Convert to XML", command=convert_file, font=("Arial", 12))
convert_button.pack(pady=10)

# Progress bar for visual feedback during conversion
progress_bar = Progressbar(root, orient=tk.HORIZONTAL, length=400, mode='determinate')
progress_bar.pack(pady=20)

# Run the Tkinter main loop
root.mainloop()


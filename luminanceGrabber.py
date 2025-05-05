import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


def listSubfolders(directory):
    """Gets the list of subfolders"""
    return [
        entry
        for entry in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, entry))
    ]


def processPngImages(folderPath):
    """Go through each png file in the folder getting the luminance from each pixel and create a file to hold that data
    Returns:
        A list of lists of the luminance information for each image"""
    pngFiles = [
        f
        for f in os.listdir(folderPath)
        if f.lower().endswith(".png") and os.path.isfile(os.path.join(folderPath, f))
    ]

    if not pngFiles:
        print("No PNGs found")
        return

    results = []

    for pngFile in pngFiles:
        imagePath = os.path.join(folderPath, pngFile)
        try:
            with Image.open(imagePath) as img:
                img = img.convert("L")
                pixels = list(img.getdata())
        except Exception as e:
            print(f"Error with {pngFile}: {e}")
            continue

        luminance = [pixel for pixel in pixels]

        baseName, _ = os.path.splitext(pngFile)
        outputFile = os.path.join(folderPath, baseName + "_luminance.txt")

        try:
            with open(outputFile, "w") as f:
                f.write("Luminance values:\n")
                f.write(str(luminance) + "\n\n")
            print(f"Processed '{pngFile}' with luminance data saved to '{outputFile}'.")
            results.append(luminance)
            # I made an implementation in case we wanted to know which file we were working with but it seemed unnesary for now
            # results.append((luminance, pngFile))
        except Exception as e:
            print(f"Could not write to file {outputFile}: {e}")
    return results


def userInterface():
    """Looks in the current directory to get the files"""
    currentDir = os.getcwd()

    folders = listSubfolders(currentDir)
    if not folders:
        print("No folders found")
        return

    print("Folders found:")
    for index, folder in enumerate(folders, start=1):
        print(f"{index}. {folder}")

    while 1:
        userInput = input(
            "Enter the number of a folder to process (q for quit): "
        ).strip()
        if userInput.lower() == "q":
            print("Quitting")
            return
        try:
            choice = int(userInput)
            if 1 <= choice <= len(folders):
                selectedFolder = folders[choice - 1]
                break
            else:
                print("Invalid number. Please choose a valid folder number")
        except ValueError:
            print("Invalid input. Please enter a number or q to quit")

    folderPath = os.path.join(currentDir, selectedFolder)
    return processPngImages(folderPath)


def graph(lum_data, wavelengths):
    incident_light = 255  # Placeholder number

    # np.clip so we don't accidentally get log(0)
    reflectance_imgs = [
        np.clip(np.array(image) / incident_light, 1e-23, 1.0) for image in lum_data
    ]  # normalize intensity

    reflectance_array = np.array(reflectance_imgs)

    absorbance_imgs = -np.log10(reflectance_array)

    avg_abs = np.mean(absorbance_imgs, axis=1)

    plt.figure(figsize=(8, 6))  # default, can change later
    plt.plot(wavelengths, avg_abs)
    plt.title("Absorbance vs Wavelength")
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Absorbance")
    plt.show()


def main():
    # graph(userInterface()) or graph(processPngImages(FOLDER PATH HERE))

    # Each image needs to associate with a specific wavelength btw
    wavelengths = [
        405,  # Purple
        436,  # Blue
        480,  # Light Blue
        530,  # Green
        550,  # Light Green/Yellow
        580,  # Yellow
        605,  # Orange
    ]  # We will have to modify this based on our ACTUAL wavelengths

    lum_data = userInterface()

    graph(lum_data, wavelengths)


if __name__ == "__main__":
    main()

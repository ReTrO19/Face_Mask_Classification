import os
from tqdm import tqdm
import cv2
import xml.etree.ElementTree as ET

def extract_face(xml_folder_path,image_folder_path,new_data_path):
    """
    Function extracts faces from the images using the annotions xml 

    :param xml_folder_path: Path to the annotations folder
    :param image_folder_path: Path to the images folder
    :param new_data_path: Path to the data folder

    :return None
    """
    class_names = ['with_mask','without_mask']
    for single_class in class_names:
        try:
            os.mkdir(os.path.join(new_data_path,single_class))
        except:
            print(f"{str(single_class)} Folder Exist")
    ids = 0
    all_xml_file = os.listdir(xml_folder_path)
    for single_xml in tqdm(all_xml_file):
        file_path = os.path.join(xml_folder_path,single_xml)
#         print("Current XML file === >",file_path)
        tree = ET.parse(file_path)
        root = tree.getroot()
        img_file = os.path.join(image_folder_path,str(tree.find('filename').text))
                     
        for single_ele in tree.findall('object'):
            class_name = str(single_ele.find(".//name").text)
            x = int(single_ele.find(".//bndbox//xmin").text)
            y = int(single_ele.find(".//bndbox//ymin").text)
            x1 = int(single_ele.find(".//bndbox//xmax").text)
            y1 = int(single_ele.find(".//bndbox//ymax").text)
            
            img = cv2.imread(img_file)
            crop_img = img[y:y1, x:x1]
            resize_image = cv2.resize(crop_img,None,fx=8,fy=8)
            file_name = os.path.join(new_data_path,class_name,class_name+"_"+str(ids)+".jpg")
            cv2.imwrite(file_name,resize_image)
            ids += 1

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Input values for the extract faces function')

    parser.add_argument('--xml_path','-xp',type=str,help='Pass the path to the annotations folder',required=True)
    parser.add_argument('--img_path','-ip',type=str,help='Pass the path to the images folder',required=True)
    parser.add_argument('--data_path','-dp',type=str,help='Pass the path to the data folder',required=True)

    args = parser.parse_args()

    extract_face(args.xml_path,args.img_path,args.data_path)
#!/usr/bin/python

import numpy as np
from PIL import Image

def pad_image(noisy_image):
    # print("Padding\n")
    row = len(noisy_image)
    col = len(noisy_image[0])
    padded_image = np.zeros((row+2,col+2), dtype=np.uint16)

    padded_image[0][0]          = noisy_image[0][0]
    padded_image[0][col+1]      = noisy_image[0][col-1]
    padded_image[row+1][0]      = noisy_image[row-1][0]
    padded_image[row+1][col+1]  = noisy_image[row-1][col-1]
    for r in range(row+2):
        for c in range(col+2):
            if r > 0 and c > 0 and r < row+1 and c < col+1:
                padded_image[r][c] = noisy_image[r-1][c-1]
            if r == 0 and c > 0 and c < col+1:
                padded_image[r][c] = noisy_image[r][c-1]
            if r == row+1 and c > 0 and c < col+1:
                padded_image[r][c] = noisy_image[r-2][c-1]
            if c == 0 and r > 0 and r < row+1:
                padded_image[r][c] = noisy_image[r-1][c]
            if c == col+1 and r > 0 and r < row+1:
                padded_image[r][c] = noisy_image[r-1][c-2]
    array2txt(padded_image,"padded_image.txt")
    return padded_image

def edge_filtering(padded_image):
    # print("filtering")
    row = len(padded_image)
    col = len(padded_image[0])
    filter_image = np.zeros((row-2,col-2), dtype=np.uint16)
    for r in range(0,row-2):
        for c in range(0,col-2):
            matrix_p = padded_image[r:r+3,c:c+3]
            matrix_c = np.array([[(x-matrix_p[1][1] if (x>matrix_p[1][1]) else matrix_p[1][1]-x) for x in sub_m] for sub_m in matrix_p],dtype=np.uint16)
            matrix_c = 255 - matrix_c
            matrix_c = np.multiply(matrix_c,matrix_c,dtype=np.uint16)>>8
            matrix_c = np.multiply(matrix_c,matrix_c,dtype=np.uint16)>>8
            matrix_c = np.multiply(matrix_c,matrix_c,dtype=np.uint16)>>8
            matrix = np.multiply(matrix_c,matrix_p,dtype=np.uint16)
            filter_image[r][c] = (np.sum(matrix)>>2)/(np.sum(matrix_c)>>2)
    array2txt(filter_image,"filter_image.txt")
    return filter_image

def array2txt(arr,txt_name):
    # row = len(arr)
    # col = len(arr[0])
    file = open(txt_name,"w")
    for sub_a in arr:
        for e in sub_a:
            file.write(str(e))
            file.write(" ")
        file.write("\n")
    file.close()    


def main():
    # print("Start")
    # image --------------------------------------------
    # doc anh
    im = Image.open("lena.tif")
    im.show()
    im = np.array(im,dtype=np.double)
    h = len(im)
    w = len(im[0])

    # tao nhieu gaul
    noise = 10*np.random.normal(0,1,(h,w))

    # cong anh voi nhieu
    n_image = np.add(im,noise)

    # loai bo cac gia tri ko phai 8 bit ko dau
    n_image = np.array([[255. if e>255. else e for e in subl_a] for subl_a in n_image],dtype=np.double)
    n_image = np.array([[0. if e<0. else e for e in subl_a] for subl_a in n_image],dtype=np.double)
    
    n_image = n_image.astype(np.uint16)

    # loc anh
    f_image = edge_filtering(pad_image(n_image))

    # chuyen array thanh anh
    noise = Image.fromarray(noise)
    n_image = Image.fromarray(n_image)
    f_image = Image.fromarray(f_image)

    # chuyen anh ve den trang
    noise = noise.convert("L")
    n_image = n_image.convert("L")
    f_image = f_image.convert("L")

    # luu anh
    noise.save("noise.png")
    n_image.save("n_image.png")
    f_image.save("f_image.png")

    # hien anh ra man hinh
    noise.show()
    n_image.show()
    f_image.show()

main()
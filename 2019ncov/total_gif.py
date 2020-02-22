import imageio
import os
from main import plot_distribution
from province_city import plot_distribution
def create_gif(image_list, gif_name, duration = 1.0):
    '''
    :param image_list: 这个列表用于存放生成动图的图片
    :param gif_name: 字符串，所生成gif文件名，带.gif后缀
    :param duration: 图像间隔时间
    :return:
    '''
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))

    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)
    return

def main():
    #plot_distribution()
    #这里放上自己所需要合成的图片
    img_path = 'pic/2019'


    image_list = []
    for i in range(21, 31):
        if i < 10:
            image_list.append(img_path + '/' + '2020-01-0' + str(i) + '.png')
        else:
            image_list.append(img_path + '/' + '2020-01-' + str(i) + '.png')

    for i in range(1, 12):
        if i < 10:
            image_list.append(img_path + '/' + '2020-02-0' + str(i) + '.png')
        else:
            image_list.append(img_path + '/' + '2020-02-' + str(i) + '.png')

    #image_list = ['1.jpg', '2.jpg', '3.jpg']
    gif_name = 'gif/new.gif'
    duration = 0.5
    create_gif(image_list, gif_name, duration)

if __name__ == '__main__':
    main()

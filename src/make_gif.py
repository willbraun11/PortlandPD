from PIL import Image
import os

# Create filepaths within df directory
# srcpath = os.path.split(os.path.abspath(‘’))[0]
# rootpath = os.path.split(srcpath)[0]
# datapath = os.path.join(rootpath, ‘data/’)
# cleanpath = os.path.join(datapath, ‘cleaned/’)
# imagepath = os.path.join(rootpath, ‘images/’)

years_list = []
for i in range(47):
    if i < 9:
        years_list.append('0' + str(i+1))
    else:
        years_list.append(str(i+1))

# Vice Files:
sourcepath = '/Users/will/Desktop/Portland/Images/vice_calls_everyothermonth/Vice_Crimes_by_Month'
save_path = 'Vice_by_Month.gif'

# Total Files:
# sourcepath = '/Users/will/Desktop/Portland/Images/total_calls_everyothermonth/Total_Crimes_by_Month'
# save_path = 'Total_by_Month.gif'


def make_gif(sourcepath, years):
    frames = []
    for year in years:
        new_frame = Image.open(sourcepath+year+'.png')
        frames.append(new_frame)
    frames[0].save(save_path,
                    format='GIF',
                    append_images=frames[1:],
                    save_all=True,
                    duration=300,
                    loop=0)

make_gif(sourcepath, years_list)
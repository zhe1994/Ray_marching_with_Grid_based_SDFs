# Ray marching with grid-based signed distance functions
## Environment  
Python 3.6.3 on Anaconda 64bit  

## Features  
- [x] Grid-based SDFs renderer  
- [x] Parellel computing  
- [x] Rendering part compatible for general SDFs   
- [x] Pinhole camera implemented  
- [x] Depth (Model space) based linear interpolation for shading  
- [ ] Texture
- [ ] Lighting and shadow

## How to use  
* To use, run:  
~~~
python deploy.py --path filename
~~~
* The grid-based SDFs were generated from this project by level-set algorithm  
https://github.com/christopherbatty/SDFGen  

## Rendering results  
* Bunny from front 
<img src="./result_bunny_front.png" width="300">

* Bunny from top  
<img src="./result_bunny_top.png" width="300">

* Cube from rotated camera  
<img src="./result_cube_rotated.png" width="300">

* Teapot    
<img src="./result_teapot.png" width="300">

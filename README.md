# occlusion-handling
 
Just so that we're all on the same page I think we should stick to the following structure while we do this project. 

 ### Installation 
Please make sure you have the following requirments then create a Conda enviroment with the yml file that is provided
which has all of the libraries/frameworks I think we'll need. This is mostly to avoid any headaches for compatibility issues. 

### Requirements
- Python ≥ 3.6
- PyTorch ≥ 1.3
- [torchvision](https://github.com/pytorch/vision/) that matches the PyTorch installation.
	You can install them together at [pytorch.org](https://pytorch.org) to make sure of this.
- pycocotools: `pip install cython; pip install 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'`
- GCC ≥ 4.9(this might not be necessary. Try creating an environment from the yml file first). 

```bash
conda env create -f environment.yml
```

If you run into an issue with creating the conda environment just make sure you at least have Detecteron2 installed which you can find [here](https://github.com/facebookresearch/detectron2/blob/master/INSTALL.md). 

 
 ### Code Organization:
 This seems like a popular way to organize these kinds of projects but we can ignore some parts if need be. 
  
 [Source and examples](https://github.com/moemen95/Pytorch-Project-Template)
![alt text](utils/pics/class_diagram.png "Template Class diagram")




 

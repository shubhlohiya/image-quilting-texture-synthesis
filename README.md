# Image Quilting for Texture Synthesis & Transfer

### Course Project for CS663 - Digital Image Processing

***

This is our implementation of Texture Synthesis and Texture Transfer using Image Quilting. It is based on the [paper](./quilting.pdf) of the same name by authors Alexei Efros and William Freeman. 

## Usage

First, clone this repository using `git clone https://github.com/shubhlohiya/image-quilting-texture-synthesis.git`

#### CLI Tool:
To use the CLI tool associated with our project do the following:

* `cd code/`
* To perform Texture Synthesis use: `python main.py --synthesis -i <texture_img> -b <block_size> -o <overlap_size> -tol <tolerance>`
* To perform Texture Transfer use: `python main.py --transfer -i <target_img> -t <texture_img> -b <block_size> -o <overlap_size> -tol <tolerance> -a <alpha>`

For more details, use `python main.py -h`

&nbsp;

## Results

#### Some Results for Texture Synthesis

| **Input Image** | **Synthesized Texture**|
|:---:|:---:|
| ![](./data/t1.png) | ![](./results/synthesis/t1_b=100_o=16_t=0_1.png) |
| ![](./data/t17.jpeg) | ![](./results/synthesis/t17_b=100_o=16_t=0_1.png) |
| ![](./data/t24.jpg) | ![](./results/synthesis/t24_b=100_o=16_t=0_1.png) |
| ![](./data/t30.png) | ![](./results/synthesis/t30_b=100_o=16_t=0_1.png) |
| ![](./data/t20.png) | ![](./results/synthesis/t20_b=100_o=16_t=0_1.png) |
| ![](./data/t11.png) | ![](./results/synthesis/t11_b=100_o=16_t=0_1.png) |
| ![](./data/t27.jpg) | ![](./results/synthesis/t27_b=100_o=16_t=0_1.png) |

&nbsp;
&nbsp;
&nbsp;

#### Some Results for Texture Transfer

| **Target Image** | **Texture Image** | **Result** |
|:---:|:---:|:---:|
| ![](./data/bill-big.jpg) | ![](./data/rice.jpg) | ![](./results/transfer/bill_rice_alpha0.2_tol0.1_bs20_ov10.jpg)|
| ![](./data/lincoln.jpg) | ![](./data/t4.jpg) | ![](./results/transfer/lincoln_t4_alpha0.2_tol0.1_bs10_ov5.jpg)|
| ![](./data/tendulkar1.jpg) | ![](./data/scribble.png) | ![](./results/transfer/tendulkar_scribble_alpha0.1_tol0.1_bs10_ov5.jpg)|
| ![](./data/landscape.jpeg) | ![](./data/van_gogh.jpeg) | ![](./results/transfer/winxp_vangogh_alpha0.2_tol0.1_b15_ov7.jpg)|

**For more results, please check the [report](./report.pdf).**

***
<p align='center'>Created with :heart: by <a href="https://www.linkedin.com/in/lohiya-shubham/">Shubham Lohiya</a>, <a href="https://www.linkedin.com/in/latika-patel-1951b0196/">Latika Patel</a> & <a href="https://www.linkedin.com/in/prathmesh-bele-52a05418b/">Prathmesh Bele</a></p>

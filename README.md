# ILS-SUMM
[Note: this repo is not final. It will be updated at 26.9.2019 13:00.]
This repo contains a python implementation of the paper - "ILS-SUMM: Iterated Local Search for Unsupervised Video Summarization" (under the review of ICLR 2020).

![](Cosmus_Laundromat.gif)  
*A video summary ILS-SUMM generated from the [Cosmus Laundromat movie](https://www.youtube.com/watch?v=Y-rmzh0PI3c).*
## Get started
1. Download the code
```bash
git clone https://github.com/ICLR-2020-ILS-SUMM/ILS-SUMM.git
```
2. Copy your features and durations of your video shots into the data directory. By default, the data directory contains the fetures and durations we use for the [Cosmus Laundromat movie](https://www.youtube.com/watch?v=Y-rmzh0PI3c).

## How to run ILS-SUMM
```bash
python demo.py
```
## Example
For the [Cosmus Laundromat movie](https://www.youtube.com/watch?v=Y-rmzh0PI3c) we get the following results:
![](Solution_Visualization.png)




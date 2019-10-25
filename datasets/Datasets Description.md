# Open Source Total Distance (OSTD) Dataset

## Links to OSTD Movies: 

1. [Big Buck Bunny](http://download.blender.org/peach/bigbuckbunny_movies/big_buck_bunny_480p_surround-fix.avi)  
2. [Cosmos Laundromat](https://archive.org/download/CosmosLaundromatFirstCycle/Cosmos%20Laundromat%20-%20First%20Cycle%20%281080p%29.mp4)  
3. [Elephants Dream](https://archive.org/download/ElephantsDream/ed_1024.avi)  
4. [Sintel](http://peach.themazzone.com/durian/movies/sintel-1024-surround.mp4)   
5. [Tears of Steel](http://ftp.nluug.nl/pub/graphics/blender/demo/movies/ToS/tears_of_steel_1080p.mov)   
6. [Valkaama](http://www.valkaama.com/download.php?target=media/movie/Valkaama_1080_p.mkv)   
7. [1000 Days](http://www.mediafire.com/file/jwa35cgdmp213j3/1000_DAYS_H264_1080.mov/file)   
8. [Boy Who Never Slept](http://www.mediafire.com/file/8cfx2e097hblar1/Boy_Who_Never_Slept_-_Remastered_Full_Movie.mp4/file)   
9. [CH7](http://www.mediafire.com/file/3pghcs6h8lhix5x/CH7.mp4/file)   
10. [Honey](http://www.mediafire.com/file/7ta3q6dpdh442z6/Honey-final-180k.mp4/file)   
11. [Jathia's Wager](http://www.mediafire.com/file/pr0itqcke8z3cjd/Jathia%2527s_Wager_%25282009%2529_-_Public_Domain_Universe_-_Solomon_D._Rothman.mp4/file)   
12. [La Chute d’une Plume](http://www.mediafire.com/file/i4mm7tnr6u3v2kv/la_chute_d_une_plume_720p_sub_en_fr_es_pt.mp4/file)  
13. [Meridian](http://www.mediafire.com/file/tcxp8ei686ee7t8/Meridian_Netflix.mp4/file)  
14. [Pentagon](http://www.mediafire.com/file/hh3i59iodwf8b39/Pentagon.2008.enSubs-correct.avi/file)  
15. [Route 66](http://www.mediafire.com/file/1krgv2jmdttebdr/Route_66_-_an_American_badDream.avi/file)  
16. [Seven Dead Men](http://www.mediafire.com/file/o19b6yv40taqa88/Seven_Dead_Men.mp4/file)  
17. [Sita Sings the Blues](http://www.mediafire.com/file/q74ogbg772p79pz/SITA_SINGS_MOVIE_ONLY.mp4/file)  
18. [Star Wreck](http://www.mediafire.com/file/o772rn8sg2af56h/Star_Wreck-_In_the_Pirkinning_%2528with_subtitles_in_10_languages%2529.mp4/file)  

## OSTD Features, Shots Durations and Ground Truth
[This directory](ostd.zip) contains:
1. Shots durations (obtained   using [Ffprob](https://pypi.org/project/ffprobe/) by [this script](gt%20auxiliary%20scripts/ffprob_shot_segmentation.py)).
2. Shots features (RGB with 32 bins, extracted by [this script](gt%20auxiliary%20scripts/extract_features.py)).
3. Optimal selection of representative points that satisfies the knapsack constraints (obtained by [PuLP](https://pypi.org/project/PuLP/) using [this script](gt%20auxiliary%20scripts/PuLP_for_Knapsack_Median.py)).
4. Optimal total distance.

# SumMe for the KM task
[Links to SumMe videos](https://gyglim.github.io/me/vsum/index.html#benchmark). 
## SumMe Features, Shots Durations and Ground Truth
[This directory](summe_for_total_distance.zip) contains:
1. Shots durations, 
obtained  using [Kernel Temporal Segmentation (KTS)](https://github.com/pathak22/videoseg/tree/master/lib/kts) with this parameters: 
maxShots = 55, vmax = 1.5, lmin = 1, lmax = 300. As features for KTS we used RGB with 32 bins, extracted by [this script](gt%20auxiliary%20scripts/extract_features.py).
2. Shots features (RGB with 32 bins, extracted by [this script](gt%20auxiliary%20scripts/extract_features.py)).
3. Optimal selection of representative points that satisfies the knapsack constraints (obtained by [PuLP](https://pypi.org/project/PuLP/) using [this script](gt%20auxiliary%20scripts/PuLP_for_Knapsack_Median.py)).
4. Optimal total distance.

# TVSum for the KM task
[Links to TVSum videos](https://github.com/yalesong/tvsum). 
## TVSum Features, Shots Durations and Ground Truth
[This directory](tvsum_for_total_distance.zip) contains:
1. Shots durations, 
obtained  using [Kernel Temporal Segmentation (KTS)](https://github.com/pathak22/videoseg/tree/master/lib/kts) with this parameters: 
maxShots = 120, vmax = 2.2, lmin = 1, lmax = 400. As features for KTS we used RGB with 32 bins, extracted by [this script](gt%20auxiliary%20scripts/extract_features.py).
2. Shots features (RGB with 32 bins, extracted by [this script](gt%20auxiliary%20scripts/extract_features.py)).
3. Optimal selection of representative points that satisfies the knapsack constraints (obtained by [PuLP](https://pypi.org/project/PuLP/) using [this script](gt%20auxiliary%20scripts/PuLP_for_Knapsack_Median.py)).
4. Optimal total distance.



# Space Mission Lab 2021-22

## Team name: binaries
## Chosen theme: Life on Earth  
## Organisation name: ROBOTONIO 
## Country: Greece

# Source files for 1st part (collect data from ISS): project/part1
# Source files for 2nd part (NDVI): project/part2


# 1. Introduction  
Plants are an essential resource - we rely on them for food, water, medicine, the air we breathe, habitat, climate, and more. As trees grow, they help stop climate change by removing carbon dioxide from the air, storing carbon in the trees and soil, and releasing oxygen into the atmosphere. 
In recent years, we have constantly been following news about the disasters in the forests, primarily due to human activities (e.g. logging, deforestation, etc.) and natural disasters, such as fires. But we are not talking about the positive actions of people, such as the efforts to reforest areas (especially in large Eastern countries such as China and India), the conversion of barren lands and arable land and the advancement of technology which allows cultivation areas all year round. But what is the final balance in the annual change of green on our planet? This question is the basis of our idea. 
We have studied the changes in the flora of our planet from the last year. We also studied the ratio between different species of flora, which we know are involved to varying degrees in the absorption of carbon dioxide.

# 2. Method  
There are two parts in our project: the ISS part and the basis part. 
For the ISS part, we simple wrote the code to collect the useful data from ISS for our analysis, like images and location data. We used the Astro Pi IR computer and we received about 750 impressive near-infrared images from our planet, with our necessary data in the csv file.
For the ISS part, we wrote a more complex program, to process the images we took, to measure the NDVI. Using an amazing guide from Raspberry Pi Foundation, in each image, we resized it, increased the contrast and then created gray and color NDVI image. The process is described in more detail in Figure 1.
![Figure1](https://github.com/robotonio/Binaries/blob/main/assets/figure1.png)
After calculating the NDVI, we divided the different species of flora into the corresponding levels of the index. We used the gray NDVI images with the assumption that, if the brightness of each pixel in the gray image is in the range (200, 255) we have forest area while in the range (160, 200) we have crops or vegetation.
You can see the code of each part of our python programs in our GitHub repository.
# 3. Experiment results  

We received about 750 amazing photos. Our concern was if there were photos showing ground (without clouds), so that we could proceed with our analyzes. Indeed, although in a small percentage, we collected about 40 images, that we were able to use.
The second part of our program, which deals with NDVI, scans all the images that we collected in a folder and for each one, it calculates the level of NDVI.
To check if our program is working properly, we can ask (via the debug parameter) to display all the stages of the analysis: cleaning the perimeter frame, gray NDVI & color NDVI. An example is shown in Figure 2.
![Figure2](https://github.com/robotonio/Binaries/blob/main/assets/figure2.png)
In the next phase, after dividing the vegetation levels into "dense / forest" and "crops / human intervention", we used the gray NDVI part to measure each level. Specifically, if the index was between 230 and 255, we assume that the corresponding vegetation was " forest", while between 200 and 229, we consider as level of vegetation "crops ". We did the same with images from the samples we had taken at the beginning of the year, from Astro Pi team. The comparative results of the two measurements are shown in Figure 3.
![Figure3](https://github.com/robotonio/Binaries/blob/main/assets/figure3.png)
The above analysis shows that forest areas are declining, while arable land is increasing, as we would expect. Of course, we know that the result is not safe, as the comparison of the two different time samples come from different geographical areas. However, as we mention in the conclusions, the purpose of the experiment is to highlight the way and the process of studying the case, something that from the result we believe that we have succeeded!
# 4. Learnings
When our teacher suggested we participate in a competition, where our program will "run" in space, the idea alone excited us! We immediately started looking for our idea for our experiment and that is where our first difficulties started. We had never dealt with the Space; we are just learning programming with python ...
Our mentor helped us, suggesting that we deal with image analysis, as in our lessons we had dealt a lot with Computer Vision. We read reports from other teams and what caught our attention was the study of NDVI.
The Internet helped us understand the usefulness of the NDVI and a Raspberry Foundation guide helped us understand its technical part. Because the analysis of NDVI seemed a little more complex, we decided not to take any chances for the 2nd phase of the competition, so our program was just collecting the necessary data.
After receiving our data (and celebrating furiously for a few hours...), we proceeded to the next phase of the analysis, utilizing the guide mentioned above. We tried hard enough to adapt the guide to our experiment, we spent several hours debugging, but the result was what we were expected!
# 5. Conclusion  
The mission was completed! We received valid data from the ISS, we had images suitable for our experiment and we measured NDVI successfully. Starting from the original idea of our experiment, the result justified our assumptions, as, over time, while forests are shrinking, arable land is increasing.
Although we are optimistic as kids, we know that to reach a safe conclusion, we need to compare satellite images from the same areas, at different times, with samples from many time periods. We knew this from the beginning and because we could not draw such data, we decided to implement our idea in the form of a simulation, with the two samples we had at our disposal, the photos of the Astro Pi team and our own, even if geographically are not identical.
We also know that the ranges of NDVI values we used to separate forests from crops are a bit arbitrary. A more accurate analysis would require a more advanced and abstract model, perhaps from the field of AI (Semantic Segmentation ...). These thoughts will accompany us until our next mission!



# Army-Shooter

<p align="center">
  <img src="https://github.com/abelyo252/Army-Shooter/blob/main/resource/army_shooter_logo.png">
</p>


**Army Shooter is a computer vision project for military use. It identifies and targets human poses from a distance**.
providing accurate shooting capabilities. Easy to use and effective, it's the ultimate tool for precision targeting and gaining the upper hand in combat.[Pygame](https://github.com/pygame) [OpenCV](https://github.com/opencv/opencv) and [Mediapipe](https://github.com/google/mediapipe) libraries. 


## Installation
To install the most recent version of Army Shooter, just follow these simple instructions. If git wasn't installed on your Windows PC, get it from `https://gitforwindows.org/` or install it on linux using `sudo apt-get install git` 

`git clone https://github.com/abelyo252/Army_S.git`<br>
`cd AKeyword_Spotting/`<br>
`pip install -r requirements.txt`<br>



## Run Code

`$ python Keyword_Spotter.py`
<hr>

<p>Keyword spotting is the process of detecting specific words or phrases in a continuous stream of speech. It is a crucial component of many speech recognition systems, including virtual assistants, voice-activated devices, and automated transcription tools. The goal of keyword spotting is to accurately identify and isolate specific keywords from a large corpus of speech data. It also include Graphical user interface.</p>


<p align="center">
  <img src="https://github.com/abelyo252/AKeyword_Spotting/blob/main/image/results.jpg">
</p>

<pre> Average 0.89 sec for inference</pre>



<p align="center">
  <img src="https://github.com/abelyo252/AKeyword_Spotting/blob/main/image/gui.png">
</p>


## Usage

You can use the project by running the `key_spotter.py` file and passing an Amharic text as input. The program will detect if any of the 20 criminal words are present in the text.

## How the Model Work

First Looking at the digital signal utterances here is how a few randomly selected ones look like in time domain with the word mentioned above each plot with their log spec:

<p align="center">
  <img  src="https://github.com/abelyo252/AKeyword_Spotting/blob/main/image/raw_audio.png">
</p>

Of course, this is prior to the addition of any noise to the samples. Additionally, because the utterances rarely last a 3 full second, the length of them may be reduced depending on the strength of the signal. 



## Voice Detection

To detect the 20 Amharic criminal words in voice samples, you can use the following steps:

1. Record a voice sample of the person speaking.
2. Convert the voice sample to a 16kHz mono WAV file.
3. Use the `key_spotter.py` program to detect if any of the 20 criminal words are present in the given audio file.


--- Special thanks to Adane T. for introducing this idea to us and help us in our difficulty in this project


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributions and Feedback

We welcome contributions! Please see the [contribution guidelines](CONTRIBUTING.md).

For feature requests or bug reports, please file a [GitHub Issue](https://github.com/abelyo252/ASP_Keyword_Spotting/issues).

For general discussion or questions, please use [GitHub Discussions](https://github.com/abelyo252/ASP_Keyword_Spotting/discussions).

## Contact

For more information contact [benyohanan212@gmail.com](mailto:benyohanan212@gmail.com) with any additional questions or comments.

<!Notice!>This project is still in demo mode, thus it does not guarantee a perfect result for the provided audio sample. With tremendous admiration, we are ready to accept anybody who can make a difference.

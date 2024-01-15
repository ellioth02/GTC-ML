from typing import Any
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub

# analyzer class
class Analyzer:
    # model wrapper class
    class __Model:
        def __init__(self, handle, class_names: [str]) -> None:
            self.__handle = handle
            self.class_names = class_names

        def __call__(self, arg: Any) -> Any:
            return self.__handle(arg)
    
    # constructor
    def __init__(self, verbose: bool = False, load_YAMNet: bool = False) -> None:
        # load member variables
        self.verbose = verbose
        self.load_YAMNet = load_YAMNet
        # load models
        if self.load_YAMNet:
            # load YAMNet model
            yamnet_model_handle = 'https://tfhub.dev/google/yamnet/1'
            yamnet_model = hub.load(yamnet_model_handle)
            class_map_path = yamnet_model.class_map_path().numpy().decode('utf-8')
            yamnet_class_names = list(pd.read_csv(class_map_path)['display_name'])
            self.yamnet_model = self.__Model(yamnet_model, yamnet_class_names)
        # load gtc model
        gtc_class_names = self.__get_gtc_classes()
        saved_model_path = './saved_model'
        reloaded_model = tf.saved_model.load(saved_model_path)
        self.gtc_model = self.__Model(reloaded_model, gtc_class_names)

    # get GTC classes
    def __get_gtc_classes(self) -> [str]:
        data_frame = pd.read_csv("./dataset/meta/class_map.csv")
        categories = data_frame.to_dict()["category"].values()
        return list(categories)
    
    # analyze the waveform using the models
    def analyze_audio(self, waveform) -> (str, float):
        # Run the model, check the output.
        if self.load_YAMNet:
            # YAMNet
            scores, embeddings, spectrogram = self.yamnet_model(waveform)
            YAMNet_class_scores = tf.reduce_mean(scores, axis=0)
            YAMNet_top_class = tf.math.argmax(YAMNet_class_scores)
            YAMNet_inferred_class = self.yamnet_model.class_names[YAMNet_top_class]
            YAMNet_top_score = YAMNet_class_scores[YAMNet_top_class]
            if self.verbose:
                print(f'[YAMNet] {YAMNet_inferred_class} ({YAMNet_top_score})')
        # GTC
        gtc_results = self.gtc_model(waveform)
        gtc_top_class = tf.math.argmax(gtc_results)
        gtc_inferred_class = self.gtc_model.class_names[gtc_top_class]
        gtc_class_probabilities = tf.nn.softmax(gtc_results, axis=-1)
        gtc_top_score = gtc_class_probabilities[gtc_top_class]
        if self.verbose:
            print(f'[GTC model] {gtc_inferred_class} ({gtc_top_score})')
        # return values of GTC model
        # the inferred class name and the confidence level of the inferrence
        return (gtc_inferred_class, gtc_top_score)

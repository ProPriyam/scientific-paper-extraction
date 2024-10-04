import tensorflow as tf
import os
import shutil

# Disable tensorflow compilation warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

def classify_images(input_folder, output_folder, model_path, labels_path):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Load label file
    with tf.gfile.GFile(labels_path, 'r') as f:
        label_lines = [line.strip() for line in f]

    # Load the trained model
    with tf.gfile.FastGFile(model_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        # Iterate through all png files in the input folder
        for filename in os.listdir(input_folder):
            if filename.lower().endswith('.png'):
                image_path = os.path.join(input_folder, filename)
                
                # Read the image data
                image_data = tf.gfile.FastGFile(image_path, 'rb').read()
                
                # Run the classification
                predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
                
                # Get the top prediction
                top_prediction = predictions[0].argsort()[-1]
                predicted_label = label_lines[top_prediction]
                score = predictions[0][top_prediction]
                
                # Print file name, classification class, and confidence for all images
                print(f"File: {filename}, Class: {predicted_label}, Confidence: {score:.5f}")
                
                # If the image is classified as "line" or "scatter-line", save it
                if predicted_label == "line" or predicted_label == "scatter-line":
                    shutil.copy(image_path, os.path.join(output_folder, filename))
                    print(f"  Saved to output folder")

if __name__ == "__main__":
    input_folder = "data/image_extraction"
    output_folder = "data/isLine"
    model_path = "chart_classification_model/retrained_graph.pb"
    labels_path = "chart_classification_model/retrained_labels.txt"

    classify_images(input_folder, output_folder, model_path, labels_path)
    print("Classification complete. Check the output folder for results.")
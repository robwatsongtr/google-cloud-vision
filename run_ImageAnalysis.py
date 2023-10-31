from ImageAnalysis import ImageAnalysis

if __name__ == "__main__":
    # # analyze a single image: 
    # img_analyzer = ImageAnalysis(bucket_name = "photo-bucket_polished-studio-402920")
    # image_blob_name = 'imgs_for_tagging/IMG_4873.jpg'
    # labels = img_analyzer.analyze_image(image_blob_name)

    # print(image_blob_name)

    # if labels:
    #     for label in labels:
    #         print(label)
    # else: 
    #     print("No labels detected")

    # print()

    # analyze directory of images to console:
    img_analyzer = ImageAnalysis(bucket_name = "photo-bucket_polished-studio-402920")

    bucket_path = 'imgs_for_tagging/'

    img_analyzer.bulk_analyze_images_to_console(bucket_path)
    
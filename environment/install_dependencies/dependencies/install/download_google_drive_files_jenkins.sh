CACHE=$1

python3 ../../shared/scripts/download_google_drive_data.py word2vec $CACHE
python3 ../../shared/scripts/download_google_drive_data.py concept_definitions $CACHE
python3 ../../shared/scripts/download_google_drive_data.py paraphrase_data $CACHE
python3 ../../shared/scripts/download_google_drive_data.py off_topic_detection_files $CACHE
python3 ../../shared/scripts/download_google_drive_data.py google_drive_credentials $CACHE
python3 ../../shared/scripts/download_google_drive_data.py sif $CACHE
python3 ../../shared/scripts/download_google_drive_data.py videos $CACHE
python3 ../../shared/scripts/download_google_drive_data.py subtitles $CACHE
python3 ../../shared/scripts/download_google_drive_data.py images $CACHE
python3 ../../shared/scripts/download_google_drive_data.py BERT_models $CACHE
python3 ../../shared/scripts/download_google_drive_data.py rst_project $CACHE
python3 ../../shared/scripts/download_google_drive_data.py exercises $CACHE
python3 ../../shared/scripts/download_google_drive_data.py programming_exercises $CACHE
python3 ../../shared/scripts/download_google_drive_data.py Joint_Solution_User_Model $CACHE
python3 ../../shared/scripts/download_google_drive_data.py content_mapping_files $CACHE

cp -R  $CACHE/videos ../../controller/web/content/
cp -R  $CACHE/images ../../controller/web/content/
cp -R  $CACHE/google_drive_credentials ../../shared/google_drive_utils/
cp  $CACHE/Vu_Walkthru_Video_final.mp4 ../../controller/web/html/react/src/videos/
cp -R $CACHE/subtitles ../../controller/web/content/
cp -R $CACHE/exercises ../../content_manager/content/
cp -R $CACHE/programming_exercises ../../content_manager/content/
cp -R $CACHE/content_mapping_files/* ../../content_manager/content/
sudo rm -r ../../shared/google_drive_files
ln -s $CACHE ../../shared/google_drive_files

cp -R $CACHE/Joint_Solution_User_Model/cluster_models ../../joint_user_solution_model/user_model/
cp -R $CACHE/Joint_Solution_User_Model/datasets ../../joint_user_solution_model/
cp -R $CACHE/Joint_Solution_User_Model/saved_models ../../joint_user_solution_model/solution_verification/
cp $CACHE/Joint_Solution_User_Model/counter-fitted-vectors.txt ../../joint_user_solution_model/solution_verification/
cp -R $CACHE/Joint_Solution_User_Model/intermediate_data ../../joint_user_solution_model/solution_verification/training_scripts/

#!/usr/bin/env bash
CACHE=$1
echo $CACHE
if [[ $CACHE == '' ]]; then
 CACHE=../../shared/google_drive_files
fi
echo $CACHE
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



find $CACHE/videos  -name '*.mp4' -exec cp {} $CACHE/videos/ \;
rsync -Pa $CACHE/google_drive_credentials ../../shared/google_drive_utils/

#Note:- Please don't remove next 2 line comments, it is being used in contentfile_validation.py file for validation.
#Every copying will go after next comment.
##CONTENTS##

rsync -P $CACHE/videos/Vu_Walkthru_Video_final.mp4 ../../controller/web/html/react/src/videos/
rsync -Pa $CACHE/videos ../../controller/web/content/
rsync -Pa $CACHE/subtitles ../../controller/web/content/
rsync -Pa $CACHE/exercises ../../content_manager/content/
rsync -Pa $CACHE/programming_exercises ../../content_manager/content/
rsync -Pa $CACHE/Joint_Solution_User_Model/cluster_models ../../joint_user_solution_model/user_model/
rsync -Pa $CACHE/Joint_Solution_User_Model/datasets ../../joint_user_solution_model/
rsync -Pa $CACHE/Joint_Solution_User_Model/saved_models ../../joint_user_solution_model/solution_verification/
rsync -Pa $CACHE/Joint_Solution_User_Model/counter-fitted-vectors.txt ../../joint_user_solution_model/solution_verification/
rsync -Pa $CACHE/Joint_Solution_User_Model/intermediate_data ../../joint_user_solution_model/solution_verification/training_scripts/
rsync -Pa $CACHE/content_mapping_files ../../content_manager/content/

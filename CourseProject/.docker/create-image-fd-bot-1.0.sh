#!/bin/sh;
build_path_reestr="perpetoom";
build_image_name="fd-bot";
docker_file=$build_image_name.dockerfile
build_version="1.0";
path="./images";

printf "\n\033[33mBuilding Docker Image\033[0m\n";

if [ "$(docker images -q $build_path_reestr/$build_image_name:$build_version)" != "" ]; then
  printf "\n\033[35m Deleting image $build_image_name:$build_version\033[0m\n"
  docker images $build_path_reestr/$build_image_name:$build_version;
  docker image rm $(docker images -q $build_path_reestr/$build_image_name)
fi;

printf "\n\033[35m Creating image from $docker_file\033[0m\n"

# --no-cache
docker build --no-cache --progress=plain -t $build_path_reestr/$build_image_name:$build_version -f ./$docker_file .;

# echo "\033[35m""   Pushing image $build_image_name:$build_version""\033[0m";
# docker push $build_path_reestr/$build_image_name:$build_version;


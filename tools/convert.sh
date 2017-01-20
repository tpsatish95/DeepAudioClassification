FILES=$(find data/original -type f -name '*.au');

for i in $FILES;
  do name=`echo $i | cut -d'.' -f1`.`echo $i | cut -d'.' -f2`;
    echo $name;
    ffmpeg -i $i -map 0:0 $name.mp3;
  done

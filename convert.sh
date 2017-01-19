FILES=$(find mini-genres -type f -name '*.au');

for i in $FILES;
  do name=`echo $i | cut -d'.' -f1`.`echo $i | cut -d'.' -f2`;
    echo $name;
    ffmpeg -i $i $name.mp3;
  done

#! bin/bash

movin(){
	for j in ./*.hgt; do
		echo -e "\e[92mConverting $j...\e[39m"
		if echo $j| grep -q ".img.hgt"; then
			usgs2sdf $j
		else
			srtm2sdf $j
		fi
		echo -e "\e[96mComplete\e[39m"
	done
}

if ls | grep -q '.zip'; then
	echo "Unzipping"
	for i in ./*.zip; do
		unzip $i
		mv $i ./test/
	done
	movin
else
	echo -e "\e[93m!! No Zips Detected !!\e[39m"
	movin
fi

#! bin/bash

QTH+=(*.qth)
QTH2+=(${QTH[@]%.*})
RX=('Site1')
QTH3=(${QTH2[@]/${RX}/})

echo -n "Next Step [1,2,3]: "
read step

coverage(){
	for i in ${QTH3[@]}; do
		echo "Test: $i to ${RX}"
		if [[ ! -e $i.lcf ]]; then
			mv .lcf $i.lcf || mv *.lcf $i.lcf
		fi
		while [ -e $i.lcf ]; do
			echo -e "\e[96m Conditions Met \e[39m"
			splat -t $i.qth -t ${RX}.qth -L 6 -d ../SDF/ -R 20 -N -n > splat_log.txt
			echo -e "\e[92m  Analysis Completed \e[39m"
			mv $i.lcf ${QTH3[m+1]}.lcf
			((m++))
			if [[ -e $i.ppm ]]; then
				echo -e "\e[34m    Output has been produced \e[39m"
			else
				echo -e "\e[91m    Output has not been produced \e39m"
			fi
		done
	done
}
fresnal(){
	echo -n "Percentage of first Fresnel Zone: "
	read zone
	while [[ ! -e "${TXT[0]}" ]]; do
		echo -e "\e[93m!!! [No Site-to-Site report Found] !!!\e[39m"
		for i in ${QTH3[@]}; do
			splat -t $i.qth -r ${RX[0]}.qth -d ../SDF/ -f $freq -metric > splat_log.txt
		done
		TXT+=(./*-to-*.txt)
	done
	if [[ -e "${TXT[0]}" ]]; then
		echo -e "\e[93m!!! [Site-to-Site report Found] !!!\e[39m"
		for k in ${TXT[@]}; do
			if grep -q "$zone% of the first Fresnel zone is clear" ./$k; then
				height+=("Clear")
			elif grep -q "to clear $zone% of the first Fresnel zone" ./$k; then
				height=$(grep -B1 "to clear $zone% of the first Fresnel zone" ./$k)
			fi
			harray+=("$k:$height")
		done
		edit1+=("${harray[@]/meters*/}")
		edit2+=("${edit1[@]/-to*least/}")
		edit3+=("${edit2[@]/'./'/}")
		edit4+=("${edit3[@]// /}")
		edit5+=("${edit4[@]//[a-z]/}")
		edit6+=("${edit5[@]/'--.:'/}")
		label+=("${edit3[@]/ */}")
		alth=("${edit6[@]//[A-Z]/}")
	fi
	for i in ${QTH3[@]}; do
		for h in ${edit3[@]}; do
			if (head -1 $i.qth | grep -wq $h); then
				l=${alth[m]}
				if [[ -n $l ]]; then
					while read a; do
						echo ${a//*m/$l m};
					done < ./$i.qth > ./$i.qth.t; mv ./$i.qth{.t,}
					printf "\tHight Adjusted to $l\t\t:$i\n"
				else
					printf "\tHeight Not Adjusted\t\t:$i\n"
				fi
				((m++))
			fi
		done
	done
	for j in ${QTH3[@]}; do
		echo -e "\e[92m--- Fresnel Calculation ($j to ${RX[0]}) ---\e[39m"
		splat -t $j.qth -r ${RX[0]}.qth -d ../SDF/ -f $freq -H height_$j.png -l loss_$j.png -metric > splat_log.txt
		mv height_$j.png ./height && mv loss_$j.png ./loss
		echo -e "\e[96m--- Analysis Complete ---\e[39m"
	done
}
frequency() {
	echo -n "Frequency (MHz): "
	read freq

	while read a; do
		echo ${a//*; Frequency/$freq ; Frequency};
	done < ./splat.lrp > ./splat.lrp.t; mv ./splat.lrp{.t,}
}

reset(){
	for i in ${QTH3[@]}; do
		while read a; do
			echo ${a//*m/10 m};
		done < ./$i.qth > ./$i.qth.t; mv ./$i.qth{.t,}
	done
	echo -e "\e[95m--- Reset Complete ---\e[39m"
	rm *.txt
}

if [[ $step = 0 ]]; then
	reset
	frequency
	coverage
elif [[ $step = 1 ]]; then
	reset
	frequency
	fresnal
elif [[ $step == 'no' ]]; then
	echo "Well fine"
elif [[ $step == "reset" ]]; then
	reset
fi

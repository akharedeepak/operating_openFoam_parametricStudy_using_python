Pre_ManD=""
Man_Dirs=(0_30 5_25 10_20 15_15 20_10 25_5 30_0)
Suf_ManD=""

# Sub_Dirs=(16 20 24 32)
# unit_Sub="mgs_tkoff_converged"

SS_Dir=code


echo "running all the codes" 

for N1_Dir in ${Man_Dirs[@]} 
do

	Man_Dir="$Pre_ManD$N1_Dir$Suf_ManD"
	Path="../$Man_Dir/$SS_Dir"
	
	if [ -d "$Path" ]; then
	  echo "Running code at Path = $Path"
	  
#	  cd $Path
#	  rm *.F90
#	  cd ../../source
	  
#	  cp *.F90 $Path
#	  cp run.sh $Path
	  
	  cd $Path
	  sed -i '/#define def_Rex_CFS/s/0.2D0/1.0D0/' read_input.c
	  sed -i '/#define def_CFL/s/0.10D0/0.06D0/' read_input.c
	  cp midstart.in midstart.in1
# 	  ./run.sh
	  
	  cd ../../source
	  
	else
	  echo "Path = $Path not present"
	  
	fi

done




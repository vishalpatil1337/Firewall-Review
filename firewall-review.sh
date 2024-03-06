#/bin/bash

mkdir CDE-Source/ CDE-Destination/  OOS-Source/ OOS-Destination/

cp cde.txt CDE-Source/ 
cp cde.txt CDE-Destination/
cp oos.txt OOS-Source/
cp oos.txt OOS-Destination/

cp source.txt CDE-Source/ 
cp source.txt OOS-Source/
cp destination.txt CDE-Destination/ 
cp destination.txt OOS-Destination/

cp final1.py matching.py subnet-partitions.py CDE-Source/
cp final1.py matching.py subnet-partitions.py CDE-Destination/
cp final1.py matching.py subnet-partitions.py OOS-Source/
cp final1.py matching.py subnet-partitions.py OOS-Destination/

# CDE Source

cd CDE-Source
python final1.py source.txt output1.txt
echo ""
echo "Enter CDE Subnet File Name - cde.txt"
echo ""
python subnet-partitions.py    #  need to enter cde.txt 
python final1.py output_ips.txt output2.txt
python matching.py output1.txt output2.txt | sort -u > Final_matching_cde_source.txt
cd ..


# CDE Destination

cd CDE-Destination
python final1.py destination.txt output1.txt
echo "-----------------------------------------------------------------------------------"
echo ""
echo "Enter CDE Subnet File Name - cde.txt"
echo ""
python subnet-partitions.py    #  need to enter cde.txt 
python final1.py output_ips.txt output2.txt
python matching.py output1.txt output2.txt | sort -u > Final_matching_cde_destinaion.txt
cd ..


# Out of Scope Source

cd OOS-Source
python final1.py source.txt output1.txt
echo "-----------------------------------------------------------------------------------"
echo ""
echo "Enter CDE Subnet File Name - oos.txt"
echo ""
python subnet-partitions.py    #  need to enter oos.txt 
python final1.py output_ips.txt output2.txt
python matching.py output1.txt output2.txt | sort -u > Final_matching_oos_source.txt
cd ..

# Out of Scope Destination

cd OOS-Destination
python final1.py destination.txt output1.txt
echo "-----------------------------------------------------------------------------------"
echo ""
echo "Enter CDE Subnet File Name - oos.txt"
echo ""
python subnet-partitions.py    #  need to enter oos.txt 
python final1.py output_ips.txt output2.txt
python matching.py output1.txt output2.txt | sort -u > Final_matching_oos_destination.txt
cd ..
echo "-----------------------------------------------------------------------------------"
echo ""

python matching.py CDE-Source/Final_matching_cde_source.txt OOS-Destination/Final_matching_oos_destination.txt | sort -u > CDESourceToOOSDestination.txt
python matching.py OOS-Source/Final_matching_oos_source.txt CDE-Destination/Final_matching_cde_destinaion.txt | sort -u > OOSSourcetoCDEDestination.txt
echo ""
echo "The result of CDE Source to Out of Scope Destination is :"
cat CDESourceToOOSDestination.txt | awk 'NR==1 || !/^Matching IP Addresses and Subnets:/' 

echo ""
echo ""
echo "The result of Out of Scope Source to CDE Destination is :"
cat OOSSourcetoCDEDestination.txt | awk 'NR==1 || !/^Matching IP Addresses and Subnets:/' 








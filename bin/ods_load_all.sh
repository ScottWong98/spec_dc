#!bin/sh

echo '--- Start load cpu2006 ---'
sh bin/ods_load_cpu2006.sh

echo '--- Start load cpu2017 ---'
sh bin/ods_load_cpu2017.sh

echo '--- Start load jbb2015 ---'
sh bin/ods_load_jbb2015.sh

echo '--- Start load jvm2008 ---'
sh bin/ods_load_jvm2008.sh

echo '--- Start load ssj2008 ---'
sh bin/ods_load_ssj2008.sh


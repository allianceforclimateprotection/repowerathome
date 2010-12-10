WorkDir=`dirname "$0"`

# Min style.css
echo -ne "style.css -> style_min.css ... "
java -jar $WorkDir/yuicompressor-2.4.2.jar --type css -o $WorkDir/../static/css/style_min.css --charset utf-8 $WorkDir/../static/css/style.css
echo "done"

# Min js_libs.js
echo -ne "js_libs.js -> js_libs_min.js ... "
java -jar $WorkDir/yuicompressor-2.4.2.jar --type js -o $WorkDir/../static/js/js_libs_min.js --charset utf-8 $WorkDir/../static/js/js_libs.js
echo "done"

# Min rah.js
echo -ne "rah.js -> rah_min.js ... "
java -jar $WorkDir/yuicompressor-2.4.2.jar --type js -o $WorkDir/../static/js/rah_min.js --charset utf-8 $WorkDir/../static/js/rah.js
echo "done"

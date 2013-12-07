#include <iostream>
#include <fstream>
#include <string>
using namespace std;

const int IMAGE_NUM = 5;
const string imagesets[IMAGE_NUM] = {"combo", "galwaycity", "goes",
				     "joetouristweather", "ultrapig2004"};
const string shortImageSets[IMAGE_NUM] = {"combo", "galway", "goes", "joe",
					  "ultrapig"};
const int WEIGHT_NUM = 4;
const string weights[WEIGHT_NUM] = {"RMSE", "SSIM", "NQM error", "DCTune"};
const char shortweights[WEIGHT_NUM] = {'r', 's', 'n', 'd'};

const int METHOD_NUM = 4;
const string methods[METHOD_NUM] = {"mst", "msta", "centroid", "traditional"};

const int COMPRESSION_NUM = 2;
const char compression[COMPRESSION_NUM] = {'j', 'w'};

// This file takes "imageset weight method compression" and then creates the gnuplot text file that graphs the lagrange distortion curve compression numbers, and the same size compression numbers and if available the lagrange closest sizes compression

int main(int argv, char *argc[]) {
   if(argv < 5) {
      cout << "not enough arguments" << endl;
      cout << "imageset weight method compression" << endl;
   }
   
   int name = -1, w = -1, m = -1, c = -1;
   // checking name
   for(int i = 0; i < IMAGE_NUM; i++) {
      if(shortImageSets[i] == string(argc[1])) {
	 name = i;
      }
   }
   if(name == -1) {
      cerr << "Not a proper image set" << endl;
      for(int i = 0; i < IMAGE_NUM; i++) {
	 cerr << shortImageSets[i] << " ";
      }
      cerr << endl;
      return 1;
   }
   // checking weight
   for(int i = 0; i < WEIGHT_NUM; i++) {
      if(shortweights[i] == argc[2][0]) {
	 w = i;
      }
   }
   if(w == -1) {
      cerr << "Not a proper weight" << endl;
      for(int i = 0; i < WEIGHT_NUM; i++) {
	 cerr << shortweights[i] << " ";
      }
      cerr << endl;
      return 1;
   }
   // checking method
   for(int i = 0; i < METHOD_NUM; i++) {
      if(methods[i] == string(argc[3])) {
	 m = i;
      }
   }
   if(m == -1) {
      cerr << "Not a proper method" << endl;
      for(int i = 0; i < METHOD_NUM; i++) {
	 cerr << methods[i] << " ";	 
      }
      cerr << endl;
      return 1;
   }
   //checking compression
   for(int i = 0; i < COMPRESSION_NUM; i++) {
      if(compression[i] == argc[4][0]) {
	 c = i;
      }
   }
   if(c == -1) {
      cerr << "Not a proper compression" << endl;
      for(int i = 0; i < COMPRESSION_NUM; i++) {
	 cerr << compression[i] << " ";
      }
      cerr << endl;
      return 1;
   }

   string lagrangeC = "/data/lernerc9/withoutNQM/Lagrange/diffImages"
      + imagesets[name] + "/pgm/" + compression[c] + shortweights[w]
      + methods[m] + "/matching.txt";

   string lagrangeDC = "/data/lernerc9/Lagrange/diffImages" + imagesets[name]
      + "/pgm/" + compression[c];
   string sameSize = "/data/lernerc9/SameSize/diffImages" + imagesets[name] + "/pgm/"
      + compression[c];
   switch(m) {
      case 0: case 1: // mst and msta
	 lagrangeDC += shortweights[w];
	 sameSize += shortweights[w];
	 break;
      case 2: case 3: // centroid and traditional
	 break;
      default:
	 cerr << "you have input the wrong method" << endl;
	 return 1;
   };
   lagrangeDC += methods[m] + shortweights[0] + "/matching.txt";
   sameSize += methods[m] + "/info.txt";

   string begin = "/data/lernerc9/graphs/" + shortImageSets[name]
      + compression[c] + shortweights[w] + methods[m];
   string outName = begin + ".txt";
   ofstream out(outName.c_str());

   if(!out.is_open()) {
      cerr << "you do not have access to the data file" << endl;
      return 1;
   }
   cout << begin << endl;
   out << "set terminal png" << endl;
   out << "set output \"" << begin << shortweights[w] << ".png\"" << endl;
   out << "set xlabel \"Size (bpp)\"" << endl;
   out << "set ylabel \"Distortion (" << weights[w] << ")\"" << endl;
   out << "set style line 1 lc rgb \"#0000FF\" ps 1 pt 5" << endl;
   out << "set style line 2 lc rgb \"#FF0000\" ps 1 pt 7" << endl;
   out << "set style line 3 lc rgb \"#006400\" ps 1 pt 4" << endl;
   out << "plot \'" << sameSize << "\' \\" << endl;
   out << "using 1:"<< 2 + w << " with linespoint ls 1 title \'Same Size\', \\"
       << endl;
   out << '\'' << lagrangeDC <<"\' \\" << endl;
   out << "using 1:" << 2 + w << " with linespoint ls 2 title \'Lagrange "
       << "Distortion Curve RMSE\'";
   if(w < 2) {
      out << ", \\" << endl;
      out << '\'' << lagrangeC << "\' \\" << endl;
      out << "using 1:" << 2 + w << " with linespoint ls 3 title \'Lagrange "
	  << "closest " << weights[w] << "\'" << endl;
   }

   if(w > 0) {
      out << endl;
      out << "set output \"" << begin << shortweights[0] << ".png\"" << endl;
      out << "set xlabel \"Size (bpp)\"" << endl;
      out << "set ylabel \"Distortion (" << weights[0] << ")\"" << endl;
      out << "set style line 1 lc rgb \"#0000FF\" ps 1 pt 5" << endl;
      out << "set style line 2 lc rgb \"#FF0000\" ps 1 pt 7" << endl;
      out << "set style line 3 lc rgb \"#006400\" ps 1 pt 4" << endl;
      out << "plot \'" << sameSize << "\' \\" << endl;
      out << "using 1:"<< 2 << " with linespoint ls 1 title \'Same Size\', "
	  << "\\" << endl;
      out << '\'' << lagrangeDC <<"\' \\" << endl;
      out << "using 1:" << 2 << " with linespoint ls 2 title \'Lagrange "
	  << "Distortion Curve RMSE\'";
      if(w < 2) {
	 out << ", \\" << endl;
	 out << '\'' << lagrangeC << "\' \\" << endl;
	 out << "using 1:" << 2 << " with linespoint ls 3 title \'Lagrange "
	     << "closest " << weights[w] << "\'" << endl;
      }
   }
   return 0;
}

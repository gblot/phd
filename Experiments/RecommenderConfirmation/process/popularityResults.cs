using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IjcaiGetPopularity
{
    class Program
    {
        static List<string> experimentedMethods = new List<string>();
        static public string ROOT = @"results\";

        static void Main(string[] args)
        {
            experimentedMethods.Add("SimCN");
            experimentedMethods.Add("SimCB");
            experimentedMethods.Add("SimCO");
            experimentedMethods.Add("SimAA");


            foreach (var MET in experimentedMethods)
            {
                //File.Delete(ROOT + "Dist" + MET + ".csv");

                StreamReader file = new System.IO.StreamReader(ROOT + MET + ".csv");
                Dictionary<String, int> METDICT = new Dictionary<String, int>();


                string line;

                while ((line = file.ReadLine()) != null)
                {
                    var lineTab = line.Split(' ');

                    if (!METDICT.Keys.ToArray().Contains(lineTab[1])) METDICT[lineTab[1]] = 0;
                    METDICT[lineTab[1]]++;

                }


                var String1 = "";
                var String2 = "";
                var sortedDict = from entry in METDICT orderby entry.Value descending select entry;
                foreach (var V in sortedDict)
                {
                    String1 += V.Key + ";";
                    String2 += V.Value + ";";
                }

                using (StreamWriter sw = File.AppendText(ROOT + "Dist" + MET + ".csv"))
                {
                    sw.WriteLine(String1);
                    sw.WriteLine(String2);

                }

            }

        }
    }
}

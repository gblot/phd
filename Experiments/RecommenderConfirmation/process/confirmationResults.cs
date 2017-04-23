using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IjcaiGetStats
{
    class Program
    {

		// Here change the output file names
        static public string ROOT = @"results\";
        static public string PV = @"results\SimCatedges.csv";
        static public string nodesPop = @"results\nodesPopularity.csv";
        static public int HeadT = 1400;
        static List<string> HEAD = new List<string>();
        static List<string> experimentedMethods = new List<string>();

        static void Main(string[] args)
        {
            experimentedMethods.Add("SimCatedges2");
            experimentedMethods.Add("SimCatSimCN");
            experimentedMethods.Add("SimCatSimCB");
            experimentedMethods.Add("SimCatSimCO");
            experimentedMethods.Add("SimCatSimPA");
            experimentedMethods.Add("SimCatSimAA");

            File.Delete(ROOT + " finalStats.csv");

            foreach (var MET in experimentedMethods)
            {
                String line;
                var listCatIn = new List<string>();
                var listCatOut = new List<string>();
                var listCatFull = new List<string>();

                int nbLines = 0;
                int nbSillon = 0;
                int nbSillonniveau2 = 0;

                Dictionary<string, string> cat = new Dictionary<string, string>();
                Dictionary<string, List<String>> cat2 = new Dictionary<string, List<string>>();

                StreamReader file = new System.IO.StreamReader(PV);


                while ((line = file.ReadLine()) != null)
                {
                    var lineTab = line.Split(' ');
                    if (lineTab[0] != "***")
                    {

                        if (!cat.Keys.ToArray().Contains(lineTab[0])) cat[lineTab[0]] = "";
                        cat[lineTab[0]] += lineTab[1] + " ";

                        if (!cat.Keys.ToArray().Contains(lineTab[1])) cat[lineTab[1]] = "";
                        cat[lineTab[1]] += lineTab[0] + " ";

                    }
                }


                foreach (string S in cat.Keys)
                {
                    var tmp = cat[S].Split(' ');
                    tmp.Distinct();
                    cat2[S] = new List<String>();
                    cat2[S] = tmp.Distinct().ToList();
                }

                file = new System.IO.StreamReader(ROOT + MET + ".csv");

                while ((line = file.ReadLine()) != null)
                {
                    var lineTab = line.Split(' ');


                    if(lineTab[0] != "***")
                    {
                        if (lineTab[0] == lineTab[1]) nbSillon++;
                        if (cat2[lineTab[0]].Contains(lineTab[1]) || lineTab[0] == lineTab[1]) nbSillonniveau2++;
                        nbLines++;

                        if (!listCatIn.Contains(lineTab[0])) listCatIn.Add(lineTab[0]);
                        if (!listCatOut.Contains(lineTab[1])) listCatOut.Add(lineTab[1]);
                        if (!listCatFull.Contains(lineTab[0])) listCatFull.Add(lineTab[0]);
                        if (!listCatFull.Contains(lineTab[1])) listCatFull.Add(lineTab[1]);

                    }

                }

                var nbPTotal = 0;
                var nbP = 0;
                if (MET != "SimCatedges2")
                {
                    file = new System.IO.StreamReader(nodesPop);
                    var cpt = 0;
                    while ((line = file.ReadLine()) != null && cpt < HeadT)
                    {
                        var lineTab = line.Split(' ');
                        HEAD.Add(lineTab[0]);
                        cpt++;
                    }

                    var sousmet = MET.Substring(MET.Length - 2);

                    file = new System.IO.StreamReader(ROOT + "Sim" + sousmet + ".csv");
                    while ((line = file.ReadLine()) != null)
                    {
                        var lineTab = line.Split(' ');
                        if (HEAD.Contains(lineTab[1])) nbP++;
                        nbPTotal++;
                    }
                    var test = 0;
                }



                using (StreamWriter sw = File.AppendText(ROOT + " finalStats.csv"))
                {
                    // Write the connection in the output file
                    double pourcentage = (double) nbSillon / (double) nbLines;
                    double pourcentageN2 = (double)nbSillonniveau2 / (double)nbLines;
                    double PI = (double)nbP / (double)nbPTotal;
                    sw.WriteLine("*****" + MET + "*****");
                    sw.WriteLine ( pourcentage + "("+ nbSillon+ "/" + nbLines + ")" + "*****");
                    sw.WriteLine(pourcentageN2 + "*****");
                    sw.WriteLine(" IN: " + listCatIn.Count + " OUT: " + listCatIn.Count + " FULL" + listCatIn.Count + "*****");
                    if (MET != "SimCatedges2") sw.WriteLine(PI + "(" + nbP + "/" + nbPTotal + ")" + "*****");

                }
            }

        }
    }
}

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IjcaiGetResults
{
    class Program
    {
        static public string PV = @"documents_categories.csv";
        static public string ROOT = @"results\";
        static public string outputPath = @"results\";
        static List<string> experimentedMethods = new List<string>();

        static void addEdge(String source, String target, String Method)
        {

            using (StreamWriter sw = File.AppendText(outputPath + "SimCat" + Method + ".csv"))
            {
                // Write the connection in the output file
                sw.WriteLine(source + " " + target);

            }
        }

        static void Main(string[] args)
        {

            experimentedMethods.Add("edges2");
            experimentedMethods.Add("SimCB");
            experimentedMethods.Add("SimCO");
            experimentedMethods.Add("SimCN");
            experimentedMethods.Add("SimPA");
            experimentedMethods.Add("SimAA");

            Dictionary<string, string> expCategories    = new Dictionary<string, string>();
            List<string> expNodes         = new List<string>();

            foreach (var MET in experimentedMethods)
                File.Delete(outputPath + "SimCat" + MET +".csv");

            System.IO.StreamReader file = new System.IO.StreamReader(ROOT+"nodes.csv");
            string line;


            Console.WriteLine("*** Building NODES");

            while ((line = file.ReadLine()) != null) expNodes.Add(line);


            Console.WriteLine("*** Building CATEGORIES");

            file = new System.IO.StreamReader(PV);
            var cpt = 0;
            while ((line = file.ReadLine()) != null)
            {
                var lineTab = line.Split(',');

                if (expNodes.Contains(lineTab[0]) && !expCategories.Keys.Contains(lineTab[0]))
                {
                    cpt++;
                    expCategories[lineTab[0]] = lineTab[1];
                }

            }

            Console.WriteLine("*** Start comparing");

            

            foreach (var MET in experimentedMethods)
            {
                file = new System.IO.StreamReader(ROOT + MET + ".csv");
                while ((line = file.ReadLine()) != null)
                {
                    var lineTab = line.Split(' ');
                    try
                    {
                        addEdge(expCategories[lineTab[0]], expCategories[lineTab[1]], MET);
                    }
                    catch {
                        addEdge("*** "+lineTab[0], lineTab[1] + "NOT_FOUND", MET);
                    }
                    

                }
            }

        }
    }
}

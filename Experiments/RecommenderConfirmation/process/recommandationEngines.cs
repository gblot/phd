using RDotNet;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IjcaiTreatment
{

    class Program
    {

        static public string outputPath = @"results\Sim";
        static List<string> experimentedMethods = new List<string>();
        static REngine engine = REngine.GetInstance();
        static Dictionary<String, Dictionary<String, int>> MATRICE = new Dictionary<String, Dictionary<String, int>>();

        static void addEdge(String source, String target, String Method)
        {

            using (StreamWriter sw = File.AppendText(outputPath+ Method + ".csv"))
            {
                // Write the connection in the output file
                sw.WriteLine(source + " " + target);

            }
        }

        // CommonNeigh
        public static Double CommonNeigh(Dictionary<String, int> Xs, Dictionary<String, int> Ys)
        {
            Double sumX = 0;
            Double sumX2 = 0;
            Double sumY = 0;
            Double sumY2 = 0;
            Double sumXY = 0;

            int n = Xs.Count < Ys.Count ? Xs.Count : Ys.Count;
            int cn = 0;

            foreach (var V in Xs.Keys)
            {
                if (Xs[V] > 0 && Ys[V] > 0) cn++;
            }
            return cn;
        }


        public static Double Adamic(Dictionary<String, int> Xs, Dictionary<String, int> Ys)
        {
            Double sumX = 0;
            Double sumX2 = 0;
            Double sumY = 0;
            Double sumY2 = 0;
            Double sumXY = 0;

            int n = Xs.Count < Ys.Count ? Xs.Count : Ys.Count;
            double ad = 0;

            foreach (var V in Xs.Keys)
            {
                if (Xs[V] > 0 && Ys[V] > 0)
                {
                    var tmp = MATRICE[V].Values.ToArray().Sum();
                    ad += 1 / Math.Log(tmp);
                }
            }
            return ad;
        }

        public static Double PreferentialAttachment(Dictionary<String, int> Xs, Dictionary<String, int> Ys)
        {
            Double sumX = 0;
            Double sumX2 = 0;
            Double sumY = 0;
            Double sumY2 = 0;
            Double sumXY = 0;

            int n = Xs.Count < Ys.Count ? Xs.Count : Ys.Count;

            var XX = Xs.Values.ToArray().Sum();
            var YY = Ys.Values.ToArray().Sum();

            return XX*YY;
        }

        // Pearson-R
        public static Double Correlation(Dictionary<String,int> Xs, Dictionary<String, int> Ys)
        {

            //REngine.SetDllDirectory("C:/Program Files/R/R-3.3.2/bin/x64/R.dll");
            double[] group1Arr = Xs.Values.ToArray().Select(x => (double)x).ToArray();
            double[] group2Arr = Ys.Values.ToArray().Select(y => (double)y).ToArray();
            NumericVector group1 = engine.CreateNumericVector(group1Arr);
            engine.SetSymbol("group1", group1);
            NumericVector group2 = engine.CreateNumericVector(group2Arr);
            engine.SetSymbol("group2", group2);

            double testResult = engine.Evaluate("cor(group2,group1,method='pearson')").AsNumeric().First();

            return Math.Abs(testResult);

        }


        public static Double Cosine(Dictionary<String, int> Xs, Dictionary<String, int> Ys)
        {

            double[] group1Arr = Xs.Values.ToArray().Select(x => (double)x).ToArray();
            double[] group2Arr = Ys.Values.ToArray().Select(y => (double)y).ToArray();
            NumericVector group1 = engine.CreateNumericVector(group1Arr);
            engine.SetSymbol("group1", group1);
            NumericVector group2 = engine.CreateNumericVector(group2Arr);
            engine.SetSymbol("group2", group2);

            double testResult = engine.Evaluate("crossprod(group2, group1) / sqrt(crossprod(group2) * crossprod(group1))").AsNumeric().First();

           
            return Math.Abs(testResult);


        }

        static public string inputEdgesPath = @"C:\Users\gblo\Documents\IJCAI\results\edges.csv";
        static public string inputNodesPath = @"C:\Users\gblo\Documents\IJCAI\results\nodes.csv";


        static void Main(string[] args)
        {

            // ADD experimented methods here
            experimentedMethods.Add("AA");
            experimentedMethods.Add("CN");
            experimentedMethods.Add("CO");

            // Delete all previous results
            foreach (var MET in experimentedMethods)
                File.Delete(outputPath + MET + ".csv");

            string line;


            Dictionary<String,int> NODES = new Dictionary<String,int>();
            var cpt = 0;

 
            // Define node indexation
            System.IO.StreamReader file =
                new System.IO.StreamReader(inputNodesPath);

            while ((line = file.ReadLine()) != null)
            {
                NODES[line] = 0;
                cpt++;
            }

            // Create matrice
            file = new System.IO.StreamReader(inputNodesPath);
            while ((line = file.ReadLine()) != null)
            {
                var M = new Dictionary<String, int>();
                foreach (var i in NODES.Keys) M[i] = 0;

                MATRICE[line] = M;
            }

            
            file = new System.IO.StreamReader(inputEdgesPath);

            while ((line = file.ReadLine()) != null)
            {
                var lineTab = line.Split(' ');

                try
                {
                    MATRICE[lineTab[0]][lineTab[1]]++;
                    MATRICE[lineTab[1]][lineTab[0]]++;
                }
                catch (Exception e)
                {
                    Console.WriteLine(e);
                }

            }


            int n = MATRICE.Count;



            foreach (var MET in experimentedMethods)
            {
                var cptLoop = 0;
                foreach (var C in MATRICE.Keys)
                {
                    Double coef = -1;
                    String coefNode = "-1";
                    Double coefValue = coef;

                    foreach (var L in MATRICE.Keys)
                    {

                        if(C != L)
                        {
                            switch (MET)
                            {
                                case "CN": coef = CommonNeigh(MATRICE[C], MATRICE[L]); break;
                                case "CB": coef = Correlation(MATRICE[C], MATRICE[L]); break;
                                case "CO": coef = Cosine(MATRICE[C], MATRICE[L]); break;
                                case "PA": coef = PreferentialAttachment(MATRICE[C], MATRICE[L]); break;
                                case "AA": coef = Adamic(MATRICE[C], MATRICE[L]); break;
                            }
                            

                            if (coefValue < coef)
                            {
                                coefNode = L;
                                coefValue = coef;

                            }
                        }
                        
                    }

                    // Display
                    Console.WriteLine(C + " " + coefNode + " "+ MET+ "("+ cptLoop + ")");

                    // Write 
                    addEdge(C, coefNode,MET);

                    cptLoop++;
                }

            }

            engine.Dispose();

        }
    }
}

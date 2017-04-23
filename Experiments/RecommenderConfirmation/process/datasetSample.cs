using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using QuickGraph.Graphviz;
using Platform.Communication.Protocol.Gexf;
using System.Xml;
using System.IO;

namespace TestIjcai
{
    class Program
    {

        static public string outputEdgesPath = @"results\edges.csv";
        static public string outputNodesPath = @"results\nodes.csv";
        static public string outputStatsPath = @"results\stats.csv";

        static public List<String> connectedNodes = new List<String>(); // Final List of considered nodes 
        static public int nbUserTotal = 0;  // Total number of Users
        static public int nbUser = 0;       // Total number on considered Connections
        static public int lineNumber = 0;   // Treated lines
        static public int limitNodes = 7000;   // z

        static public List<String> userList = new List<String>();
        static public int lastNumberofNodes = 0;


        static void addEdge(String source, String target, String user, int i)
        {

            using (StreamWriter sw = File.AppendText(outputEdgesPath))
            {
                // Write the connection in the output file
                sw.WriteLine(source + " " + target);

                // Fullfill the Node structure
                if (!connectedNodes.Contains(source)) connectedNodes.Add(source);
                if (!connectedNodes.Contains(target)) connectedNodes.Add(target);

                if (!userList.Contains(user)) userList.Add(user);

                // LOG
                if (lastNumberofNodes != connectedNodes.Count)
                {
                    lastNumberofNodes = connectedNodes.Count;
                    Console.WriteLine(lastNumberofNodes+" ("+ userList.Count + ")");
                }

            }
        }

        static void addStats()
        {

            using (StreamWriter sw = File.AppendText(outputStatsPath))
            {
                sw.WriteLine("Users:" + userList.Count);

            }
        }


        static void addNode(String node)
        {

            using (StreamWriter sw = File.AppendText(outputNodesPath))
            {
                sw.WriteLine(node);
            }
        }

        static void Main(string[] args)
        {

            File.Delete(outputEdgesPath);
            File.Delete(outputNodesPath);
            File.Delete(outputStatsPath);

            string PV   = @"C:\Users\gblo\Documents\IJCAI\page_views.csv";
            int FLOATING_WINDOW      = 50000;
            int IT = 100;
            
            string line;

            var userListCurrent     = new List<String>();
            var userListPrevious    = new List<String>();

            var userDictPair = new Dictionary<String, List<String>>();
            var userDictImPair = new Dictionary<String, List<String>>();

            string LastNode = "";


            for (int i = 0; i < IT; i++)
            {

                var cpt = 0;

                System.IO.StreamReader file =
                    new System.IO.StreamReader(PV);

                if(i%2 == 0) userDictPair = new Dictionary<String, List<String>>();
                else userDictImPair = new Dictionary<String, List<String>>();

                while ((line = file.ReadLine()) != null && cpt < (FLOATING_WINDOW * IT) * 100)
                {

                    var lineTab = line.Split(',');

                    if (cpt > i * FLOATING_WINDOW)
                    {
                     
                        switch (i%2)
                        {
                            case 0:
                                if (userDictPair.ContainsKey(lineTab[0]))
                                {
                                    addEdge(userDictPair[lineTab[0]][userDictPair[lineTab[0]].Count - 1], lineTab[1], lineTab[0], i);
                                    userDictPair[lineTab[0]].Add(lineTab[1]);

                                }
                                else
                                {
                                    if (userDictPair.Count < FLOATING_WINDOW && !userDictImPair.ContainsKey(lineTab[0]))
                                    {
                                        var list = new List<String>();
                                        list.Add(lineTab[1]);
                                        userDictPair.Add(lineTab[0], list);
                                    }

                                }
                                break;
                            case 1:
                                if (userDictImPair.ContainsKey(lineTab[0]))
                                {
                                    addEdge(userDictImPair[lineTab[0]][userDictImPair[lineTab[0]].Count - 1], lineTab[1], lineTab[0], i);
                                    userDictImPair[lineTab[0]].Add(lineTab[1]);
                                }
                                else
                                {
                                    if (userDictImPair.Count < FLOATING_WINDOW && !userDictPair.ContainsKey(lineTab[0]))
                                    {
                                        var list = new List<String>();
                                        list.Add(lineTab[1]);
                                        userDictImPair.Add(lineTab[0], list);
                                    }

                                }
                                break;
                        }
                        
                    }

                    cpt++;

                    if (connectedNodes.Count >= limitNodes) break;


                }


                file.Close();

                if (connectedNodes.Count >= limitNodes) break;

            }

            // Display Connected nodes
            foreach (var node in connectedNodes) addNode(node);

            addStats();
            
        }
    }
}

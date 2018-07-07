import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

/**
 * To create Apache Lucene index in a folder and add files into this index based
 * on the input of the user.
 */
public class HW4 {
    private static Analyzer analyzer = new SimpleAnalyzer(Version.LUCENE_47);
	static String systemName = "JSYLucene";
    private IndexWriter writer;
    private ArrayList<File> queue = new ArrayList<File>();

    public static void main(String[] args) throws IOException {
	System.out
		.println("Enter the FULL path where the index will be created: (e.g. /Usr/index or c:\\temp\\index)");

	String indexLocation = null;
	BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
	String s = br.readLine();

		//delete current files in the directory to ensure previous generated index wont effect current results
		//Note: this piece code only deletes files and not child directories.
		File f = new File(s);
		File files[] = f.listFiles();
		for (File ef:
			 files) {
			ef.delete();
		}

		HW4 indexer = null;
	try {
	    indexLocation = s;
	    indexer = new HW4(s);
	} catch (Exception ex) {
	    System.out.println("Cannot create index..." + ex.getMessage());
	    System.exit(-1);
	}

	// ===================================================
	// read input from user until he enters q for quit
	// ===================================================
	while (!s.equalsIgnoreCase("q")) {
	    try {
		System.out
			.println("Enter the FULL path to add into the index (q=quit): (e.g. /home/mydir/docs or c:\\Users\\mydir\\docs)");
		System.out
			.println("[Acceptable file types: .xml, .html, .html, .txt]");
		s = br.readLine();
		if (s.equalsIgnoreCase("q")) {
		    break;
		}

		// try to add file into the index
		indexer.indexFileOrDirectory(s);
	    } catch (Exception e) {
		System.out.println("Error indexing " + s + " : "
			+ e.getMessage());
	    }
	}

	// ===================================================
	// after adding, we always have to call the
	// closeIndex, otherwise the index is not created
	// ===================================================
	indexer.closeIndex();

	// =========================================================
	// Now search
	// =========================================================
	IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(
		indexLocation)));
	IndexSearcher searcher = new IndexSearcher(reader);


		String scoreDoc = "LuceneDocScore.txt";
		File file = new File(scoreDoc);
		FileWriter fw = null;
		BufferedWriter bw = null;

		if (!file.exists()) {
			try {
				file.createNewFile();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		try {
			fw = new FileWriter(file.getAbsoluteFile());
			bw = new BufferedWriter(fw);
		} catch (IOException e) {
			e.printStackTrace();
		}

	s = "";

		System.out.println("Query File Path:");
		String qf = br.readLine();
		//parsing the queries from given files
		Map<Integer, String> qm = new HashMap<>();
		Integer key = 0;
		StringBuilder sb = new StringBuilder();
		try (BufferedReader br2 = new BufferedReader(new FileReader(qf)))
		{

			String sCurrentLine;
			Boolean startFlag = false;

			while ((sCurrentLine = br2.readLine()) != null) {
				if(sCurrentLine.contains("<DOC>")) {
					startFlag = true;

				}
				else if(sCurrentLine.contains("<DOCNO>") && sCurrentLine.contains("</DOCNO>") && startFlag) {
					String newLine = sCurrentLine.replace("<DOCNO>", "");
					String newLine2 = newLine.replace("</DOCNO>", "");
					String number = newLine2.replaceAll("\\s","");
					key = Integer.parseInt(number);
				}
				else if(sCurrentLine.contains("</DOC>") && startFlag )
				{
					startFlag = false;
					qm.put(key, sb.toString());
					key = 0;
					sb = new StringBuilder();
				}
				else if(startFlag)
				{
					sb.append(sCurrentLine);
				}

			}

		} catch (IOException e) {
			e.printStackTrace();
		}


		for (Map.Entry<Integer, String> qe:qm.entrySet()){
			System.out.println(qe.getValue());
			TopScoreDocCollector collector = TopScoreDocCollector.create(100, true);
	    s = qe.getValue();
			Query q = null;
			try {
				q = new QueryParser(Version.LUCENE_47, "contents",
                    analyzer).parse(QueryParser.escape(s));
			} catch (ParseException e) {
				e.printStackTrace();
			}
			searcher.search(q, collector);
		ScoreDoc[] hits = collector.topDocs().scoreDocs;

		// 4. display results
		System.out.println("Found " + hits.length + " hits.");
		for (int i = 0; i < hits.length; ++i) {
		    int docId = hits[i].doc;
		    Document d = searcher.doc(docId);
			File fn = new File(d.get("path"));
			bw.write(qe.getKey()+" "+"Q0"+" "+fn.getName().replaceAll(".txt","")+" "+(i+1)+" "+hits[i].score+" "+ systemName);
			bw.newLine();
		}
	}
	bw.close();

    }

    /**
     * Constructor
     * 
     * @param indexDir
     *            the name of the folder in which the index should be created
     * @throws IOException
     *             when exception creating index.
     */
    HW4(String indexDir) throws IOException {

	FSDirectory dir = FSDirectory.open(new File(indexDir));

	IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47,
		analyzer);

	writer = new IndexWriter(dir, config);
    }

    /**
     * Indexes a file or directory
     * 
     * @param fileName
     *            the name of a text file or a folder we wish to add to the
     *            index
     * @throws IOException
     *             when exception
     */
    public void indexFileOrDirectory(String fileName) throws IOException {
	// ===================================================
	// gets the list of files in a folder (if user has submitted
	// the name of a folder) or gets a single file name (is user
	// has submitted only the file name)
	// ===================================================
	addFiles(new File(fileName));

	int originalNumDocs = writer.numDocs();
	for (File f : queue) {
	    FileReader fr = null;
	    try {
		Document doc = new Document();

		// ===================================================
		// add contents of file
		// ===================================================
		fr = new FileReader(f);
		doc.add(new TextField("contents", fr));
		doc.add(new StringField("path", f.getPath(), Field.Store.YES));
		doc.add(new StringField("filename", f.getName(),
			Field.Store.YES));

		writer.addDocument(doc);
		System.out.println("Added: " + f);
	    } catch (Exception e) {
		System.out.println("Could not add: " + f);
	    } finally {
		fr.close();
	    }
	}

	int newNumDocs = writer.numDocs();
	System.out.println("");
	System.out.println("************************");
	System.out
		.println((newNumDocs - originalNumDocs) + " documents added.");
	System.out.println("************************");

	queue.clear();
    }

    private void addFiles(File file) {

	if (!file.exists()) {
	    System.out.println(file + " does not exist.");
	}
	if (file.isDirectory()) {
	    for (File f : file.listFiles()) {
		addFiles(f);
	    }
	} else {
	    String filename = file.getName().toLowerCase();
	    // ===================================================
	    // Only index text files
	    // ===================================================
	    if (filename.endsWith(".htm") || filename.endsWith(".html")
		    || filename.endsWith(".xml") || filename.endsWith(".txt")) {
		queue.add(file);
	    } else {
		System.out.println("Skipped " + filename);
	    }
	}
    }

    /**
     * Close the index.
     * 
     * @throws IOException
     *             when exception closing
     */
    public void closeIndex() throws IOException {
	writer.close();
    }
}
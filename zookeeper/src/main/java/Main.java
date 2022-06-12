import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
            if (args.length < 2)
            {
                System.err.println("ARGUMENTS ERROR: should be Exectur IP:port program [arguments...]");
                System.exit(1);
            }

            String IPAndPort = args[0];
            String[] exec = new String[args.length - 1];
            String znode = "/z";
            System.arraycopy(args, 1, exec, 0, exec.length);

            Executor executor = new Executor(IPAndPort, znode, exec, 5000);
            BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
            System.out.println("Write 'tree' to print current znodes tree, and s to stop");
            while (executor.isRunning())
            {
                try
                {
                    String line = br.readLine();
                    if (line.equals("tree"))
                        executor.listChildren();
                    else if (line.equals("s")) {
                        executor.stop();
                    }
                    else
                        System.out.println("Unrecognized command.");
                }
                catch (IOException e)
                { e.printStackTrace(); }
            }
        }
}

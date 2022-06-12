import org.apache.zookeeper.*;
import org.apache.zookeeper.data.Stat;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Stack;

public class Executor implements Watcher, AsyncCallback.StatCallback {
    private final ZooKeeper serviceConnection;
    private final String znode;
    private final String[] execPath;
    private Process execProcess;
    private boolean dead = false;

    public Executor(String ipAndPort, String znode, String[] exec, int timeout) throws IOException {
        this.znode = znode;
        this.execPath = exec;
        this.serviceConnection = new ZooKeeper(ipAndPort, timeout, this);
        try {
            serviceConnection.addWatch(znode, AddWatchMode.PERSISTENT_RECURSIVE);
        } catch (KeeperException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        serviceConnection.exists(znode, true, this, null);
    }

    public void run() {
        try {
            synchronized (this) {
                while (!dead) {
                    wait();
                }
            }
        } catch (InterruptedException e) {
        }
    }

    public void closing(int rc) {
        synchronized (this) {
            notifyAll();
        }
    }

    @Override
    public void process(WatchedEvent event) {
        String path = event.getPath();
        System.out.println(event + ", " + path);

        if(event.getState() == Event.KeeperState.Expired){
            stop();
            return;
        }

        if(event.getPath().equals(this.znode)){
            switch (event.getType()){
                case NodeCreated:
                    startExec();
                    break;
                case NodeDeleted:
                    stopExec();
                    break;
                default:
                    break;
            }
            return;
        }

        if(event.getPath().startsWith(this.znode)){
            switch (event.getType()){
                case NodeCreated:
                case NodeDeleted:
                    printChildrenNumber(znode);
                    break;
                default:
                    break;
            }
        }
    }

    @Override
    public void processResult(int rc, String path, Object ctx, Stat stat) {
        switch (rc) {
            case KeeperException.Code.Ok -> startExec();
            case KeeperException.Code.NoNode -> stopExec();
            case KeeperException.Code.SessionExpired, KeeperException.Code.NoAuth -> {
                stop();
            }
            default -> serviceConnection.exists(znode, true, this, null);
        }
    }

    public void listChildren() {
        ArrayList<String> nodeTreeStructure = getNodeTreeStructure(znode);
        for(String execProcess : nodeTreeStructure){
            System.out.println(execProcess);
        }
    }

    private void printChildrenNumber(String znode) {
        try {
            System.out.println(serviceConnection.getAllChildrenNumber(znode));
        } catch (KeeperException e) {
            e.printStackTrace();
        } catch (InterruptedException e){
            e.printStackTrace();
        }
    }

    private void stopExec() {
        if(execProcess != null){
            execProcess.destroy();
            execProcess = null;
        }
    }

    private void startExec() {
        try {
            execProcess = Runtime.getRuntime().exec(execPath);
        } catch (IOException e){
            e.printStackTrace();
        }
    }


    private ArrayList<String> getNodeTreeStructure(String nodePath){
        ArrayList<String> nodeTreeStructure = new ArrayList<>();
        try {
            this.nodeDFS(nodePath, nodeTreeStructure);
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (KeeperException e) {
            e.printStackTrace();
        }
        return nodeTreeStructure;
    }

    private void nodeDFS(String nodePath, ArrayList<String> nodeTreeStructure) throws InterruptedException, KeeperException {
        Stack<String> nodeDFSStack = new Stack<>();
        nodeDFSStack.push(nodePath);
        while(!nodeDFSStack.empty()){
            String currentRootPath = nodeDFSStack.pop();
            for(String execProcessPath : serviceConnection.getChildren(currentRootPath, false)){
                nodeDFSStack.push(String.join("/", currentRootPath, execProcessPath));
            }
            nodeTreeStructure.add(currentRootPath);
        }
    }


    public boolean isRunning() {
        return !dead;
    }

    public void stop() {
        dead = true;
    }
}

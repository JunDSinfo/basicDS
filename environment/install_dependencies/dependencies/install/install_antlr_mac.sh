
cd /usr/local/lib
sudo curl -O https://www.antlr.org/download/antlr-4.7.2-complete.jar
export CLASSPATH=".:/usr/local/lib/antlr-4.7.2-complete.jar:$CLASSPATH"
alias antlr4='java -jar /usr/local/lib/antlr-4.7.2-complete.jar'
alias grun='java org.antlr.v4.gui.TestRig'

echo 'You should extend the CLASSPATH system variable and set the aliases antlr4 and grun in your bash'
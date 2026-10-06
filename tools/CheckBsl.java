import org.antlr.v4.runtime.*;
import com.github._1c_syntax.bsl.parser.*;
class CheckBsl {
 public static void main(String[] args) throws Exception {
  int[] errors = {0};
  BaseErrorListener listener = new BaseErrorListener() {
   public <T extends Token> void syntaxError(Recognizer<T, ?> r, T s, int line, int pos, String msg, RecognitionException e) {
    errors[0]++; System.err.println(line+":"+pos+" "+msg);
   }
  };
  for (String name : args) {
   BSLLexer lexer = new BSLLexer(CharStreams.fromFileName(name));
   lexer.addErrorListener(new ANTLRErrorListener<Integer>() {
    public <T extends Integer> void syntaxError(Recognizer<T, ?> r, T symbol, int line, int pos, String msg, RecognitionException e) {
     errors[0]++; System.err.println(name + ":" + line + ":" + pos + " " + msg);
    }
   });
   BSLParser parser = new BSLParser(new IncrementalTokenStream(lexer));
   parser.removeErrorListeners(); parser.addErrorListener(listener);
   parser.file();
   System.out.println(name + ": parsed");
  }
  if (errors[0] > 0) System.exit(1);
 }
}

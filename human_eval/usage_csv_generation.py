from eval_csv_code import create_eval_csv

#CHat GPT
#es;fr;it;no;sv;ar;ru;uk

#Google 
#es;fr;it;no;sv;ar;ru;uk

#for lang in ["es", "it", "no", "ar"]:
#    create_eval_csv("gpt-4o_processed.csv", lang)
    
    
for lang in ["fr", "sv", "ru", "uk"]:
    create_eval_csv("google_processed.csv", lang)
    

```
ExeGen
│  .gitignore
│  process.py   # Run this file to generate exercises
│  readme.md
│  requirements.txt
├─ablation experiment   #Code used for ablation experiments
│      process_no_discriminator.py
│      process_no_generator.py
│      process_no_knowledgechain.py
│      process_no_kt.py
│      process_no_regeneration.py
│      
├─bert  
│  │  vocab.txt
│  │  
│  └─bert-base-chinese
│          config.json
│          pytorch_model.bin
│          
├─experiment    #Code used for the experiment
│      baseline.py
│      create_prompt.py
│      dataSet.py
│      ECR.py
│      gene_explanation.py
│      knowledge_extraction.py
│      LLM_SCORE.py
│      new.py
│      process_deepseek.py
│      process_Llama.py
│      process_Qwen_max.py
│      process_Qwen_plus.py
│      process_Qwen_turbo.py
│      test_Multiple_Choice.py
│      test_Single_Choice.py
│      test_TrueorFalse.py
│      
├─graph
│      fig(1).py
│      figcompare.py
│      figstu.py
│      layer L(1).py
│      layer.py
│      rader_graph.py
│      
├─output
│      output12248.txt
│      output17360.txt
│      output17500.txt
│      output24880.txt
│      questionnaire.txt
│      user1.txt
│      
├─processed_data(1)
│      challenge2id.pkl
│      challenge2topic.txt
│      course2challenge.txt
│      course2id.pkl
│      course2topic.txt
│      course_info.txt
│      user2challenge.txt
│      user2course.txt
│      user2id.pkl
│      
├─subject_data(1)   #Dataset
│      concept.csv
│      concept_relationship.csv
│      concept_relationship_filtered.csv
│      course_concept.csv
│      course_exercise.csv
│      course_problem.csv
│      course_profile.csv
│      error.txt
│      example.csv
│      examples_with_explanation(short).csv
│      examples_with_explanation.csv
│      examples_with_explanation_with_tokens.csv
│      problem.csv
│      problem_concept.csv
│      stuRec.csv
│      stuRec_1000.csv
│      stuRec_1000_with_tokens.csv
│      user_course.csv
│      user_problem.csv
│      user_profile.csv
│      
├─testData
│      course_concepts.csv
│      course_profile.csv
│      problem_profile.csv
│      user_problem.csv
│      user_profile.csv
│      
├─txtfile   #Results of the experiment
│      case_study.txt
│      case_study_stu.txt
│      compare.zip
│      error.txt
│      fig.png
│      fig1.png
│      fig2.png
│      fig3.png
│      figcompare.png
│      figcompare.zip
│      figcomparenew.png
│      figcomparenewstu.png
│      figcomparestu.png
│      figcomparestu.zip
│      figcomparetogether.png
│      figcomparetogether.zip
│      figstu.png
│      figstu.zip
│      formet.txt
│      java_kt_example.txt
│      Judgment_Qwen_f2.png
│      judgment_Qwen_pre6.png
│      judgment_rader.png
│      j_output.txt
│      multiple_choice_Qwen_pre6.png
│      Multiple_Qwen_f2.png
│      multiple_rader.png
│      n_output.txt
│      prompt.txt
│      ques-res.txt
│      requirements.txt
│      res.txt
│      result-questionnaire.txt
│      result_complete.txt
│      result_complete_4o_mul.txt
│      result_complete_4o_sin.txt
│      result_complete_4o_ToF.txt
│      result_deepseek_sin.txt
│      result_Llama_mul.txt
│      result_Llama_sin.txt
│      result_Llama_ToF.txt
│      result_no_discriminator_4o.txt
│      result_no_generator_4o.txt
│      result_no_knowledgechain_4o.txt
│      result_no_kt_4o.txt
│      result_no_regeneration_4o.txt
│      result_Qwen_max_mul.txt
│      result_Qwen_max_sin.txt
│      result_Qwen_max_ToF.txt
│      result_Qwen_plus_mul.txt
│      result_Qwen_plus_sin.txt
│      result_Qwen_plus_ToF.txt
│      result_Qwen_turbo_mul.txt
│      result_Qwen_turbo_sin.txt
│      result_Qwen_turbo_ToF.txt
│      single_choice_Qwen_pre6.png
│      Single_Qwen_f2.png
│      single_rader.png
│      temp.py
│      test.txt
│      专家评判.txt
│      双折线.zip
│      学生评判.txt
│      对比评判.txt
│      折线.zip
│      柱状图.zip
│      雷达图.zip
│      
├─webapp
│      questionnaire_result.py
│      result.txt
│      tea_process_complete.py
│      tea_process_no_discriminator.py
│      
└─__pycache__
```

## Quick Start

```
python3 process.py --type_of_prompt json_text --exercise_type Single_Choice --output_type json --Number_of_Generations 10
```
- --type_of_prompt : Format of the input reference data set
- --exercise_type : Type of exercises to be generated
- --output_type : Format of the output exercise
- --Number_of_Generations : Number of exercises generated
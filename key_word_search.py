# import pickle
# import pandas as pd
# import numpy as np
# from sentence_transformers import SentenceTransformer
#
# # Load model and data
# sentence_file = open("sentence", "rb")
# sentence = pickle.load(sentence_file)
# sentence_embedding_file = open("sentence_embedding", "rb")
# sentence_embedding = pickle.load(sentence_embedding_file)
# sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
#
# # Processing text to paragraphs
# f = open('Principles.txt', 'r')
# docs = f.read()
# paragraph_list = docs.split('\n\n')
# para_list = []
# for i in paragraph_list:
#     if len(i) > 0:
#         para_list.append(i)
#     else:
#         pass
#
#
# def cosine(u, v):
#     return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
#
#
# class KeyWordSearch:
#      def query(self, text_query):
#         query_vec = sbert_model.encode([text_query])[0]
#         result = []
#         for sen, embedding in zip(sentence, sentence_embedding):
#             dict_temp = {}
#             similarity = cosine(query_vec, embedding)
#             dict_temp['sen'] = sen
#             dict_temp['similarity'] = similarity
#             for para in para_list:
#                 if sen in para:
#                     dict_temp['paragraph'] = para
#                     break
#             result.append(dict_temp)
#         df = pd.DataFrame.from_dict(result)
#         df_top5 = df.sort_values(by='similarity', ascending=False).head(5)
#         df_final = df_top5[df_top5.duplicated() == False]
#         paragraphs = df_final['paragraph'].to_list()
#         paragraph_json = {'principle': paragraphs}
#         print(paragraph_json)
#         return paragraph_json
#
#
# if __name__ == "__main__":
#     a = KeyWordSearch()
#     a.query("it is raining")

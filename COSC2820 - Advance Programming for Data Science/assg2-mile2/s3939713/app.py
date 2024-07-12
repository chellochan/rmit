from flask import Flask, render_template, request, redirect, Response
import logging

import pickle
from module.Utils import *
from gensim.models.fasttext import FastText

logging.basicConfig(filename='record.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__)

job_ad_path_template = "./data/{category}/Job_{file_index}.txt"

result = read_job_ad()
g_job_ad_list = result[0]
g_job_ad_category = result[1]
g_job_ad_category_dict = {}
for cat in g_job_ad_category:
    g_job_ad_category_dict[cat] = category_to_display(cat)

ft_model = FastText.load("job_ad_model.model")
with open('lr_model.pkl', 'rb') as file:
    lr_model = pickle.load(file)

seed = 0


@app.route('/')
def index():
    app.logger.debug("job ad list len:{}".format(len(g_job_ad_list)))
    app.logger.debug("job_ad_category:{}".format(g_job_ad_category))
    return render_template('home.html', job_ad_list=g_job_ad_list)


@app.route('/job/<web_index>')
def job_detail(web_index):
    job_ad = find_job_ad_by_web_index(g_job_ad_list, web_index)
    if job_ad:
        return render_template('job_detail.html', job_ad=job_ad, job_ad_cat_dict=g_job_ad_category_dict)
    else:
        return render_template('job_detail_error.html', web_index=web_index)


@app.route('/category')
def category():
    category_job_ad_dict = {}
    for job_ad in g_job_ad_list:
        app.logger.debug("dict: {}".format(category_job_ad_dict.keys()))
        app.logger.debug("job_ad.job_category:{}".format(job_ad.job_category))

        if job_ad.job_category in category_job_ad_dict.keys():
            app.logger.debug("job_ad.job_category:{}".format(job_ad.job_category))
            app.logger.debug("display job category:{}".format(category_job_ad_dict[job_ad.job_category]))
            category_job_ad_dict[job_ad.job_category].append(job_ad)
        else:
            category_job_ad_dict[job_ad.job_category] = [job_ad]
            app.logger.debug("category_job_ad_dict:{}".format(category_job_ad_dict))
    app.logger.debug("dict len: {}".format(len(category_job_ad_dict)))
    return render_template('category.html', len=len(category_job_ad_dict), category_job_ad_dict=category_job_ad_dict, display_category_dict=g_job_ad_category_dict)


@app.route('/employer', methods=['GET', 'POST'])
def employer():
    if request.method == 'POST':
        latest_webIndex = get_latest_webIndex(g_job_ad_list)
        f_title = request.form['title']
        f_company = request.form['company']
        f_salary = request.form['salary']
        f_desc = request.form['description']
        f_category = request.form['category']
        app.logger.debug("title:{}, company:{}, desc:{}".format(f_title, f_company, f_desc))
        job_ad_data = "Title: {title}\nWebindex: {webIndex}\nCompany: {company}\nSalary: {salary}\nDescription: {desc}"
        job_ad_data = job_ad_data.format(title=f_title, webIndex=latest_webIndex, company=f_company, salary=f_salary, desc=f_desc)
        file_index = len(g_job_ad_list) + 1
        file_path = job_ad_path_template.format(category=f_category, file_index=str(file_index).rjust(5, '0'))
        pre_job_ad = JobAd(file_path, job_ad_data, f_category)
        with open(file_path, "w+", encoding="utf=8") as f:
            f.write(job_ad_data)

        g_job_ad_list.append(pre_job_ad)
        return redirect('job/{}'.format(latest_webIndex))
    else:
        return render_template('employer.html', job_ad_category=g_job_ad_category_dict)


@app.route('/employer/category/suggest', methods=['POST'])
def category_suggest():
    f_title = request.form['title']
    f_desc = request.form['description']
    fake_raw_data = "Title: {title}\nDescription: {desc}"
    raw_data = fake_raw_data.format(title=f_title, desc=f_desc)
    pred_job_ad = JobAd(None, raw_data, None)
    pred_job_ad.tokenizeTitle()
    pred_job_ad.tokenizeDesc()
    app.logger.debug("tokens:{}".format(pred_job_ad.all_tokens))

    pred_word_vec = generate_word_vector_for_modelling(pred_job_ad, ft_model)

    arr = []
    g_job_ad_list.sort(key=lambda jobAd: int(jobAd.get_web_index()))
    for job_ad in g_job_ad_list:
        job_dict = {}
        job_dict["web_idx"] = job_ad.get_web_index()
        job_dict["title"] = job_ad.get_title()
        job_dict["category"] = job_ad.job_category
        job_dict["desc_tokens"] = job_ad.desc_tokens
        job_dict["title_tokens"] = job_ad.title_tokens
        job_dict["all_tokens"] = job_ad.all_tokens
        arr.append(job_dict)

    columns = ["web_idx", "title", "category", "desc_tokens", "title_tokens", "all_tokens"]
    df_job_ad = pd.DataFrame(arr, columns=columns)

    predict_cat = predict_category(lr_model, pred_word_vec, df_job_ad['category'])
    app.logger.debug("predict: {}".format(predict_cat))
    response = Response(predict_cat, content_type='text/plain')
    return response


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')


if __name__ == '__main__':
    app.run()

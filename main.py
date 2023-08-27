import os
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from dotenv import load_dotenv
from datetime import datetime

from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_KEY")
ckeditor = CKEditor(app)
bootstrap = Bootstrap5(app)
    

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")
db = SQLAlchemy()
db.init_app(app)


class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    subtitle = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    body = db.Column(db.Text, nullable=False)
    date = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)

    comments = relationship("Art_Comment", back_populates="parent_article")


class Video(db.Model):
    __tablename__ = "videos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, nullable=False)
    thumbnail = db.Column(db.String, nullable=False)
    vid_url = db.Column(db.String, nullable=False)

    comments = relationship("Vid_Comment", back_populates="parent_video")


class Art_Comment(db.Model):
    __tablename__ = "art_comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), nullable=False)

    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"))
    parent_article = relationship("Article", back_populates="comments")


class Vid_Comment(db.Model):
    __tablename__ = "vid_comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), nullable=False)

    video_id = db.Column(db.Integer, db.ForeignKey("videos.id"))
    parent_video = relationship("Video", back_populates="comments")


class CommentForm(FlaskForm):
    comment = CKEditorField(label="Comment", validators=[DataRequired()])
    submit = SubmitField(label="Submit Comment")


gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    art = db.get_or_404(Article, 1)
    vid = db.get_or_404(Video, 1)
    return render_template("index.html", art=art, vid=vid)


@app.route('/news')
def get_all_news():
    result = db.session.execute(db.Select(Article).order_by(Article.id))
    articles = result.scalars().all()
    return render_template("news.html", articles=articles)


@app.route('/get_news/<int:news_id>', methods=['GET', 'POST'])
def get_news(news_id):
    form = CommentForm()
    result = db.session.execute(db.Select(Article).where(Article.id == news_id))
    art = result.scalar()
    if form.validate_on_submit():
        comment = Art_Comment(
            text = form.comment.data,
            parent_article = art
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('get_news', news_id=news_id))
    # print(art.body.split('\n'))
    return render_template("get_news.html", art=art, form=form)


@app.route('/videos')
def get_all_videos():
    result = db.session.execute(db.Select(Video).order_by(Video.id))
    videos = result.scalars().all()
    return render_template("videos.html", videos=videos)


@app.route('/get_vid/<int:vid_id>', methods=['GET','POST'])
def get_video(vid_id):
    form = CommentForm()
    result = db.session.execute(db.Select(Video).where(Video.id == vid_id))
    vid = result.scalar()
    if form.validate_on_submit():
        comment = Vid_Comment(
            text = form.comment.data,
            parent_video = vid
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('get_video', vid_id=vid_id))
    return render_template("get_vid.html", vid=vid, form=form)


@app.route('/shop')
def get_all_items():
    return render_template("shop.html")


@app.route('/setup')
def setup():
    a = Article(
        title="What Does Ozempic Mean for Body Positivity?",
        subtitle="Opinions on the Correlation between Ozempic and Body Positivity",
        author="Raven Smith",
        body=
        '''I understand the attraction to Ozempic, a prescription medication used for the management of Type 2 diabetes that's gone mainstream. The weekly injection offers the seemingly impossible: making and keeping you thin. You don't have to be careful or eat clean or even mindfully—you just jab and go. It's not unlike other drugs that have started out medicinal before turning recreational. (A reminder here to club kids that some horses do actually need tranquilizing.)
        We'll all enthralled, enjoying the hype, the who's-on-it sleuth-ery of Ozempic. I too am guilty of zooming in on selfies, Poirot-ing for signs of meds-induced shrinkage. We're absorbing the telltale faces, caved in from a body that's changing too quickly.
        But then there's the insidious ideology that this latest weight-loss drug pushes. Societal misconceptions about obesity and un-slimness abound: Anyone bigger than you eats more than you, moves less that you, can't control themselves. We ignore the correlation between obesity and wealth—the time and money it takes to dodge processed foods. We're still tangled up in the idea that restraint is willpower, that weight is as simple as what calories you put into your body versus what you work off.
        At the same time, we've paid lip service to body acceptance, we've go-girl-ed larger women, we've celebrated curves, we've recognized the gargantuan societal factors in how people look, we quote-unquote did the work. But now with Ozempic, being overweight can instantly (if expensively) be fixed. Larger people can swiftly transition to a more societally acceptable size. Ozempic is a miracle drug, a cure for the fatness we've begrudgingly forced ourselves to accept. 
        I know I'm being glib, but in recent times we've watched the conversation around bodies change for the better, for the more understanding, for the more realistic…and now we're all, erm, excited to fix the problem ASAP? A problem we all agreed wasn't a problem? We've yo-yoed our progression.
        I guess, depressingly, that the power of thin hasn't waned. I hate the idea, pushed by this jab, that your best self is thinner, leaner, than your current self. I hate the idea that fat is fine for other people, but not for me. That yass girl, I accept your decisions—but I'm gonna jab myself to stay thin. That fatness is something to work on and eventually overcome. Ozempic encourages us to focus on a mantra of eat, but for God's sake, don't grow. It's all quite grim.
        Despite a new drug that offers the quickest of fixes, I hope you're able to resist another pull toward being thinner, this slide backward toward smallness. Ozempic tackles the physicality of fatness without addressing obesity, the same way chemotherapy tackles lung cancer but doesn't address smoking. Taking Ozempic doesn't help us to work on our societal prejudice against obesity and the scrutiny of a person's looks. Fatness itself isn't the problem—we are.''',
        date="March 8, 2023",
        img_url="https://assets.vogue.com/photos/6408ee98de6e601dc4966a05/4:3/w_1920,c_limit/GettyImages-1308622864.jpg"
    )
    b = Article(
        title="The Importance of Adaptive Fashion",
        subtitle="Why Indonesian Fashion Industry Needs to Focus More on Adaptive Fashion",
        author="Ilman Ramadhanu",
        body=
        '''Fashion has historically been an industry that relies on exclusionary practices. Because of this, many marginalised communities have not been considered a top priority by the fashion industry, particularly the disability community. 
        “I sometimes wish that clothes don't have too many buttons on them,” said Ilma, a 26-year-old project assistant with cerebral palsy and a wheelchair user when asked about her experience when shopping for clothes. “Because I have problems with my motoric skills, it's harder for me to do the buttons and it takes me a long time to do them.”
        Button is only one of the issues she finds in clothing as she further described her clothing options to be limited, specifically because many brands and retailers still haven't incorporated the needs of people with disabilities into their designs. 
        “Sometimes I would see a cute dress, but then I see the zipper is in the back and that makes it harder for me to wear because I couldn't reach it. Also, as someone who uses a wheelchair, sometimes the issue is the clothes are too tight and that makes it harder for me to put them on and take them off, so I usually just find clothes that are easy for me to wear,” she explained.
        These are also experienced by other people with disabilities. Ilma told the story of her deaf friend who struggles to find hijabs with fabrics that would not impair her hearing aid. “Perhaps it is because the fabric is too thick, so she always has to find a way to shape the hijab in a way that it won't disturb her hearing aid.”''',
        date="January 19, 2023",
        img_url="https://images.squarespace-cdn.com/content/v1/5af1298bfcf7fd60f31f66bd/c773aa4d-3c08-42e0-a70f-84499e962d19/ADAPTIVE+FASHION.png?format=1500w"
    )
    c = Article(
            title="Citayam Fashion Week",
            subtitle="Jakarta's Budget Fashionistas Get their Turn on the Catwalk",
            author="Hellena Souisa and Natasya Salim",
            body=
            '''Muhamad Rizqi's catwalk is a zebra crossing, with traffic lights instead of spotlights.
            As he struts for the cameras in stilettos, a skin-tight polka-dot jumpsuit and trench coat, the applause of Jakarta's glitterati crowded on the footpaths is mixed with the sound of honking horns from passing cars. 
            Citayam Fashion Week — an organic fashion phenomenon based around a crosswalk near the Dukuh Atas station and park area in Central Jakarta — is the hot new thing in Indonesia's capital, and Muhamad is one of its stars.
            "At first when I looked on social media, I thought, what is this place? Why are these people going there?" the 21-year-old told the ABC.
            "But after I went there, it turned out that the people, even though they just met, were friendly and fun, the interactions were beyond what was seen on social media."
            However, many in conservative Indonesia — including some in government — are not fans of Muhamad's style.
            Dukuh Atas is a transport hub in Jakarta's CBD where trains from the outer suburbs like Citayam, Bogor, and Bekasi meet with the city's bus lines and other routes.
            The provincial government redeveloped the area in 2019, creating a public park, pedestrianising a road and building a skate park.
            It's one of the few places in greater Jakarta with public open space. About nine per cent of central Jakarta is public open green space while outer areas like Citayam and Bekasi are about 6 to 7 per cent.
            The name Citayam Fashion Week — it's not a "week" as such — started out as a tongue-in-cheek label for the custom of less-well-off young people from outer-Jakarta areas like Citayam to dress up and go to Dukuh Atas to hang out. 
            Sometimes they would pretend the crosswalk was a catwalk, and post interviews with each other on TikTok.''',
            date="August 7, 2022",
            img_url="https://live-production.wcms.abc-cdn.net.au/8687f08fec25f58b9897098083937666?impolicy=wcms_crop_resize&cropH=720&cropW=1080&xPos=0&yPos=0&width=862&height=575"
        )
    db.session.add(a)
    db.session.add(b)
    db.session.add(c)
    db.session.commit()

    x = Video(
        title="The Ultimate Guide to Finding Jeans for YOUR Body Type | Style Lesson With TLC | 2023 Guide",
        author="The Lifestyle Cog",
        thumbnail="https://img.youtube.com/vi/DOjCrrrGa5s/maxresdefault.jpg",
        vid_url="https://www.youtube.com/embed/DOjCrrrGa5s?si=jU2FqawOrnbEkGyD"
    )
    y = Video(
        title="HOW TO MAKE YOUR OUTFITS BETTER | elevate your daily style ✨",
        author="Asia Jackson",
        thumbnail="https://img.youtube.com/vi/klKVm1FALhs/maxresdefault.jpg",
        vid_url="https://www.youtube.com/embed/klKVm1FALhs?si=m3VM4k25Z1ti4VFx"        
    )
    z = Video(
        title="What's Your Style? | Ep.68 | What's The Juice? Podcast",
        author="What's The Juice?",
        thumbnail="https://img.youtube.com/vi/oUWhNZb1AdQ/maxresdefault.jpg",
        vid_url="https://www.youtube.com/embed/oUWhNZb1AdQ?si=MsQH-MHTpd0bF_3N"  
    )
    db.session.add(x)
    db.session.add(y)
    db.session.add(z)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
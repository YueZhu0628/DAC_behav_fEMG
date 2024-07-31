// Questionnaires


// ****************************************************************************
// *                                 Constants                                *
// ****************************************************************************

// tab name
var title = document.querySelector('title');
title.innerText = 'DACFE Survey';

// full screen
var fs = { 
  type: 'fullscreen', 
  fullscreen_mode: true,
  on_start: function(){
    document.body.style.background = "white";
    document.body.style.color = 'black'   
  }
};

// ID
jsPsych.data.addProperties({
  subject: jsPsych.randomization.randomID(10), 
  date: Date(),
});

// ****************************************************************************
// *                                 Start                                    *
// ****************************************************************************

var PID;
var PID_ID = {
  type: 'survey-text',
  questions: [
    {prompt: "Please enter your Participant ID", name:'PID', required: true},
    ],
  on_finish: function(data) {
    PID  = JSON.parse(data.responses)['PID'];
    jsPsych.data.addProperties({
      'PID':   JSON.parse(data.responses)['PID'],
    });
  }
};


// ****************************************************************************
// *                               Instructions                               *
// ****************************************************************************

var start_inst = {
  type: 'instructions', 
  pages: [
      'Thank you for completing the first part of the study! <br>\
       We would now like you to answer questions about your attitudes and yourself. <br>\
       Please take your time to answer each question carefully and honestly. <br>\
       Your responses are completely <b>confidential<b>.'
       ], 
       show_clickable_nav: true
};

var end_screen = {
  type: 'html-keyboard-response',
  stimulus: `Thank you for your participation! You are now finished the entire study. <br> \
             <br> \
             <b> Please do not close this page. <br> Please inform your experimenter. <b> <br>\
             <br> \ 
       <b> EXPERIMENTER: PRESS "SPACEBAR" TO SAVE THE DATA <b>
             `,
  choices: ['escape','space'],
};


// ****************************************************************************
// *                               Questionnaires                               *
// ****************************************************************************

// BISBAS
var likert_scale = ['Very true for me','Some what true for me','Some what false for me','Very false for me']

var BISBAS = {
  // see https://local.psy.miami.edu/people/faculty/ccarver/availbale-self-report-instruments/bisbas-scales/
  type: 'survey-likert',
  
  preamble: '<br> Here are some statement that a person may either agree with or disagree with.  \
            For each item, indicate how much you agree or disagree with what it says.  \
            Please respond to all the items; do not leave any blank.  \
            Choose only one response to each statement.  \
            Please be as accurate and honest as you can be. <br>',
  questions: [
    {prompt: "A person's family is the most important thing in life.", name:'BAI1', required: true, labels:likert_scale},
    {prompt: "Even if something bad is about to happen to me, I rarely experience fear or nervousness.", name:'BAI2', required: true, labels: likert_scale},
    {prompt: "I go out of my way to get things I want.", name:'BAI3', required: true, labels: likert_scale},
    {prompt: "When I'm doing well at something I love to keep at it.", name:'BAI4', required: true, labels: likert_scale},
    {prompt: "I'm always willing to try something new if I think it will be fun.", name:'BAI5', required: true, labels: likert_scale},
    {prompt: "How I dress is important to me.", name:'BAI6', required: true, labels: likert_scale},
    {prompt: "When I get something I want, I feel excited and energized.", name:'BAI7', required: true, labels: likert_scale},
    {prompt: "Criticism or scolding hurts me quite a bit.", name:'BAI8', required: true, labels: likert_scale},
    {prompt: "When I want something I usually go all-out to get it.", name:'BAI9', required: true, labels: likert_scale},
    {prompt: "I will often do things for no other reason than that they might be fun.", name:'BAI10', required: true, labels: likert_scale},
    {prompt: "It's hard for me to find the time to do things such as get a haircut.", name:'BAI11', required: true, labels: likert_scale},
    {prompt: "If I see a chance to get something I want I move on it right away.", name:'BAI12', required: true, labels: likert_scale},
    {prompt: "I feel pretty worried or upset when I think or know somebody is angry at me.", name:'BAI13', required: true, labels: likert_scale},
    {prompt: "When I see an opportunity for something I like I get excited right away.", name:'BAI14', required: true, labels: likert_scale},
    {prompt: "I often act on the spur of the moment.", name:'BAI15', required: true, labels: likert_scale},
    {prompt: "If I think something unpleasant is going to happen I usually get pretty worked up.", name:'BAI16', required: true, labels: likert_scale},
    {prompt: "I often wonder why people act the way they do.", name:'BAI17', required: true, labels: likert_scale},
    {prompt: "When good things happen to me, it affects me strongly.", name:'BAI18', required: true, labels: likert_scale},
    {prompt: "I feel worried when I think I have done poorly at something important.", name:'BAI19', required: true, labels: likert_scale},
    {prompt: "I crave excitement and new sensations.", name:'BAI20', required: true, labels: likert_scale},
    {prompt: "When I go after something I use a no holds barred approach.", name:'BAI21', required: true, labels: likert_scale},
    {prompt: "I have very few fears compared to my friends.", name:'BAI22', required: true, labels: likert_scale},
    {prompt: "It would excite me to win a contest.", name:'BAI23', required: true, labels: likert_scale},
    {prompt: "I worry about making mistakes.", name:'BAI24', required: true, labels: likert_scale},
    ],
  
  on_finish: function(data) {
    jsPsych.data.addProperties({
      BAI1_filler:     JSON.parse(data.responses)['BAI1'],
      BAI2_bis:     JSON.parse(data.responses)['BAI2'],
      BAI3_bas_d:     JSON.parse(data.responses)['BAI3'],
      BAI4_bas_rr:     JSON.parse(data.responses)['BAI4'],
      BAI5_bas_fs:     JSON.parse(data.responses)['BAI5'],
      BAI6_filler:     JSON.parse(data.responses)['BAI6'],
      BAI7_bas_rr:     JSON.parse(data.responses)['BAI7'],
      BAI8_bis:     JSON.parse(data.responses)['BAI8'],
      BAI9_bas_d:     JSON.parse(data.responses)['BAI9'],
      BAI10_bas_fs:    JSON.parse(data.responses)['BAI10'],
      BAI11_filler:    JSON.parse(data.responses)['BAI11'],
      BAI12_bas_d:    JSON.parse(data.responses)['BAI12'],
      BAI13_bis:    JSON.parse(data.responses)['BAI13'],
      BAI14_bas_rr:    JSON.parse(data.responses)['BAI14'],
      BAI15_bas_fs:    JSON.parse(data.responses)['BAI15'],
      BAI16_bis:    JSON.parse(data.responses)['BAI16'],
      BAI17_filler:    JSON.parse(data.responses)['BAI17'],
      BAI18_bas_rr:    JSON.parse(data.responses)['BAI18'], 
      BAI19_bis:    JSON.parse(data.responses)['BAI19'],
      BAI20_bas_fs:    JSON.parse(data.responses)['BAI20'],
      BAI21_bas_d:    JSON.parse(data.responses)['BAI21'],
      BAI22_bis:    JSON.parse(data.responses)['BAI22'],
      BAI23_bas_rr:    JSON.parse(data.responses)['BAI23'],
      BAI24_bis:    JSON.parse(data.responses)['BAI24']
    });
  }
};

// NFC
var likert_scale = ['Extremely uncharacteristic','2','3','4','Extremely characteristic']

var NFC = {
  // see https://centerofinquiry.org/uncategorized/need-for-cognition-scale-wabash-national-study/
  type: 'survey-likert',
  preamble: '<br><br> For each of the statements below, please indicate to what extent the statement \
            is characteristic of you.',
  scale_width: 500, 
  
  questions: [
    {prompt: "I would prefer complex to simple problems.", name:'NFC1', required: true, labels: likert_scale},
    {prompt: "I like to have the responsibility of handling a situation that requires a lot of thinking.", name:'NFC2', required: true, labels:likert_scale},
    {prompt: "Thinking is not my idea of fun.", name:'NFC3', required: true, labels:likert_scale},
    {prompt: "I would rather do something that requires little thought than something that is sure to challenge my thinking abilities.", name:'NFC4', required: true, labels:likert_scale},
    {prompt: "I try to anticipate and avoid situations where there is likely a chance I will have to think in depth about something.", name:'NFC5', required: true, labels:likert_scale},
    {prompt: "I find satisfaction in deliberating hard and for long hours.", name:'NFC6', required: true, labels:likert_scale},
    {prompt: "I only think as hard as I have to.", name:'NFC7', required: true, labels:likert_scale},
    {prompt: "I prefer to think about small, daily projects to long-term ones.", name:'NFC8', required: true, labels:likert_scale},
    {prompt: "I like tasks that require little thought once I’ve learned them.", name:'NFC9', required: true, labels:likert_scale},
    {prompt: "The idea of relying on thought to make my way to the top appeals to me.", name:'NFC10', required: true, labels:likert_scale},
    {prompt: "I really enjoy a task that involves coming up with new solutions to problems.", name:'NFC11', required: true, labels:likert_scale},
    {prompt: "Learning new ways to think doesn’t excite me very much.", name:'NFC12', required: true, labels:likert_scale},
    {prompt: "I prefer my life to be filled with puzzles that I must solve.", name:'NFC13', required: true, labels:likert_scale},
    {prompt: "The notion of thinking abstractly is appealing to me.", name:'NFC14', required: true, labels:likert_scale},
    {prompt: "I would prefer a task that is intellectual, difficult, and important to one that is somewhat important but does not require much thought.", name:'NFC15', required: true, labels:likert_scale},
    {prompt: "I feel relief rather than satisfaction after completing a task that required a lot of mental effort.", name:'NFC16', required: true, labels:likert_scale},
    {prompt: "It’s enough for me that something gets the job done; I don’t care how or why it works.", name:'NFC17', required: true, labels:likert_scale},
    {prompt: "I usually end up deliberating about issues even when they do not affect me personally.", name:'NFC18', required: true, labels:likert_scale}
      ],

  on_finish: function(data) {
    jsPsych.data.addProperties({
      NFC1:     JSON.parse(data.responses)['NFC1'],
      NFC2:     JSON.parse(data.responses)['NFC2'],
      NFC3:     JSON.parse(data.responses)['NFC3'],
      NFC4:     JSON.parse(data.responses)['NFC4'],
      NFC5:     JSON.parse(data.responses)['NFC5'],
      NFC6:     JSON.parse(data.responses)['NFC6'],
      NFC7:     JSON.parse(data.responses)['NFC7'],
      NFC8:     JSON.parse(data.responses)['NFC8'],
      NFC9:     JSON.parse(data.responses)['NFC9'],
      NFC10:    JSON.parse(data.responses)['NFC10'],
      NFC11:    JSON.parse(data.responses)['NFC11'],
      NFC12:    JSON.parse(data.responses)['NFC12'],
      NFC13:    JSON.parse(data.responses)['NFC13'],
      NFC14:    JSON.parse(data.responses)['NFC14'],
      NFC15:    JSON.parse(data.responses)['NFC15'],
      NFC16:    JSON.parse(data.responses)['NFC16'],
      NFC17:    JSON.parse(data.responses)['NFC17'],
      NFC18:    JSON.parse(data.responses)['NFC18']
    });
  }
};

// BFI
var likert_scale = ['Disagree strongly','2','3','4','Agree strongly']

var BFI = {
  // see https://arc.psych.wisc.edu/self-report/big-five-inventory-bfi/
  type: 'survey-likert',
  
  preamble: '<br><br> Here are a number of characteristics that may or may not apply to you. \
            <br> For example, do you agree that you are someone who likes to spend time with others? \
            <br> Please indicate the extent to which you agree or disagree with that statement.  <br>',
  questions: [
    {prompt: "Talks a lot.", name:'BFI1', required: true, labels:likert_scale},
    {prompt: "Notices other people’s weak points.", name:'BFI2', required: true, labels: likert_scale},
    {prompt: "Does things carefully and completely.", name:'BFI3', required: true, labels: likert_scale},
    {prompt: "Is sad, depressed.", name:'BFI4', required: true, labels: likert_scale},
    {prompt: "Is original, comes up with new ideas.", name:'BFI5', required: true, labels: likert_scale},
    {prompt: "Keeps their thoughts to themselves.", name:'BFI6', required: true, labels: likert_scale},
    {prompt: "Is helpful and not selfish with others.", name:'BFI7', required: true, labels: likert_scale},
    {prompt: "Can be kind of careless.", name:'BFI8', required: true, labels: likert_scale},
    {prompt: "Is relaxed, handles stress well.", name:'BFI9', required: true, labels: likert_scale},
    {prompt: "Is curious about lots of different things.", name:'BFI10', required: true, labels: likert_scale},
    {prompt: "Has a lot of energy.", name:'BFI11', required: true, labels: likert_scale},
    {prompt: "Starts arguments with others.", name:'BFI12', required: true, labels: likert_scale},
    {prompt: "Is a good, hard worker.", name:'BFI13', required: true, labels: likert_scale},
    {prompt: "Can be tense; not always easy going.", name:'BFI14', required: true, labels: likert_scale},
    {prompt: "Clever; thinks a lot.", name:'BFI15', required: true, labels: likert_scale},
    {prompt: "Makes things exciting.", name:'BFI16', required: true, labels: likert_scale},
    {prompt: "Forgives others easily.", name:'BFI17', required: true, labels: likert_scale},
    {prompt: "Isn’t very organized.", name:'BFI18', required: true, labels: likert_scale},
    {prompt: "Worries a lot.", name:'BFI19', required: true, labels: likert_scale},
    {prompt: "Has a good, active imagination.", name:'BFI20', required: true, labels: likert_scale},
    {prompt: "Tends to be quiet.", name:'BFI21', required: true, labels: likert_scale},
    {prompt: "Usually trusts people.", name:'BFI22', required: true, labels: likert_scale},
    {prompt: "Tends to be lazy.", name:'BFI23', required: true, labels: likert_scale},
    {prompt: "Doesn’t get upset easily; steady.", name:'BFI24', required: true, labels: likert_scale},
    {prompt: "Is creative and inventive.", name:'BFI25', required: true, labels: likert_scale},
    {prompt: "Has a good, strong personality.", name:'BFI26', required: true, labels: likert_scale},
    {prompt: "Can be cold and distant with others.", name:'BFI27', required: true, labels: likert_scale},
    {prompt: "Keeps working until things are done.", name:'BFI28', required: true, labels: likert_scale},
    {prompt: "Can be moody.", name:'BFI29', required: true, labels: likert_scale},
    {prompt: "Likes artistic and creative experiences.", name:'BFI30', required: true, labels: likert_scale},
    {prompt: "Is kind of shy.", name:'BFI31', required: true, labels: likert_scale},
    {prompt: "Kind and considerate to almost everyone.", name:'BFI32', required: true, labels: likert_scale},
    {prompt: "Does things quickly and carefully.", name:'BFI33', required: true, labels: likert_scale},
    {prompt: "Stays calm in difficult situations.", name:'BFI34', required: true, labels: likert_scale},
    {prompt: "Likes work that is the same every time.", name:'BFI35', required: true, labels: likert_scale},
    {prompt: "Is outgoing; likes to be with people.", name:'BFI36', required: true, labels: likert_scale},
    {prompt: "Is sometimes rude to others.", name:'BFI37', required: true, labels: likert_scale},
    {prompt: "Makes plans and sticks to them.", name:'BFI38', required: true, labels: likert_scale},
    {prompt: "Get nervous easily.", name:'BFI39', required: true, labels: likert_scale},
    {prompt: "Likes to think and play with ideas.", name:'BFI40', required: true, labels: likert_scale},
    {prompt: "Doesn’t like artistic things (plays, music).", name:'BFI41', required: true, labels: likert_scale},
    {prompt: "Likes to cooperate; goes along with others.", name:'BFI42', required: true, labels: likert_scale},
    {prompt: "Has trouble paying attention.", name:'BFI43', required: true, labels: likert_scale},
    {prompt: "Knows a lot about art, music and books.", name:'BFI44', required: true, labels: likert_scale},
    ],
  
  on_finish: function(data) {
    jsPsych.data.addProperties({
      BFI1_ext: JSON.parse(data.responses)['BFI1'],
      BFI2_agr: JSON.parse(data.responses)['BFI2'],
      BFI3_con: JSON.parse(data.responses)['BFI3'],
      BFI4_neu: JSON.parse(data.responses)['BFI4'],
      BFI5_open: JSON.parse(data.responses)['BFI5'],
      BFI6_ext: JSON.parse(data.responses)['BFI6'],
      BFI7_agr: JSON.parse(data.responses)['BFI7'],
      BFI8_con: JSON.parse(data.responses)['BFI8'],
      BFI9_neu: JSON.parse(data.responses)['BFI9'],
      BFI10_open: JSON.parse(data.responses)['BFI10'],
      BFI11_ext: JSON.parse(data.responses)['BFI11'],
      BFI12_agr: JSON.parse(data.responses)['BFI12'],
      BFI13_con: JSON.parse(data.responses)['BFI13'],
      BFI14_neu: JSON.parse(data.responses)['BFI14'],
      BFI15_open: JSON.parse(data.responses)['BFI15'],
      BFI16_ext: JSON.parse(data.responses)['BFI16'],
      BFI17_agr: JSON.parse(data.responses)['BFI17'],
      BFI18_con: JSON.parse(data.responses)['BFI18'],
      BFI19_neu: JSON.parse(data.responses)['BFI19'],
      BFI20_open: JSON.parse(data.responses)['BFI20'],
      BFI21_ext: JSON.parse(data.responses)['BFI21'],
      BFI22_agr: JSON.parse(data.responses)['BFI22'],
      BFI23_con: JSON.parse(data.responses)['BFI23'],
      BFI24_neu: JSON.parse(data.responses)['BFI24'],
      BFI25_open: JSON.parse(data.responses)['BFI25'],
      BFI26_ext: JSON.parse(data.responses)['BFI26'],
      BFI27_agr: JSON.parse(data.responses)['BFI27'],
      BFI28_con: JSON.parse(data.responses)['BFI28'],
      BFI29_neu: JSON.parse(data.responses)['BFI29'],
      BFI30_bas_rr: JSON.parse(data.responses)['BFI30'],
      BFI31_ext: JSON.parse(data.responses)['BFI31'],
      BFI32_agr: JSON.parse(data.responses)['BFI32'],
      BFI33_con: JSON.parse(data.responses)['BFI33'],
      BFI34_neu: JSON.parse(data.responses)['BFI34'],
      BFI35_open: JSON.parse(data.responses)['BFI35'],
      BFI36_ext: JSON.parse(data.responses)['BFI36'],
      BFI37_agr: JSON.parse(data.responses)['BFI37'],
      BFI38_con: JSON.parse(data.responses)['BFI38'],
      BFI39_neu: JSON.parse(data.responses)['BFI39'],
      BFI40_open: JSON.parse(data.responses)['BFI40'],
      BFI41_open: JSON.parse(data.responses)['BFI41'],
      BFI42_agr: JSON.parse(data.responses)['BFI42'],
      BFI43_con: JSON.parse(data.responses)['BFI43'],
      BFI44_open: JSON.parse(data.responses)['BFI44']
    });
  }
};


// UPPS-P
var likert_scale = ['Strongly agree','2','3','Strongly disagree']

var UPPS_P = {
// see https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4055534/
  type: 'survey-likert',
  preamble: '<br><br> Below are a number of statement that describe ways in which \
            people act and think. \
            <br> For each statement, please indicate how much you \
            agree or disagree with it. Be sure to indicate your agreement or disagreement \
            for every statement below.',
  scale_width: 500, 
  
  questions: [
    {prompt: "I generally like to see things through to the end.", name:'UPPS1', required: true, labels: likert_scale},
    {prompt: "My thinking is usually careful and purposeful.", name:'UPPS2', required: true, labels:likert_scale},
    {prompt: "When I am in great mood, I tend to get into situations that could cause me problems.", name:'UPPS3', required: true, labels:likert_scale},
    {prompt: "Unfinished tasks really bother me.", name:'UPPS4', required: true, labels:likert_scale},
    {prompt: "I like to stop and think things over before I do them.", name:'UPPS5', required: true, labels:likert_scale},
    {prompt: "When I feel bad, I will often do things I later regret in order to make myself feel better now.", name:'UPPS6', required: true, labels:likert_scale},
    {prompt: "Once I get going on something I hate to stop.", name:'UPPS7', required: true, labels:likert_scale},
    {prompt: "Sometimes when I feel bad, I can't seem to stop what I am doing even though it is making me feel worse.", name:'UPPS8', required: true, labels:likert_scale},
    {prompt: "I quite enjoy taking risks.", name:'UPPS9', required: true, labels:likert_scale},
    {prompt: "I tend to lose control when I am in a great mood.", name:'UPPS10', required: true, labels:likert_scale},
    {prompt: "I finish what I start.", name:'UPPS11', required: true, labels:likert_scale},
    {prompt: "I tend to value and follow a rational, 'sensible' approach to things.", name:'UPPS12', required: true, labels:likert_scale},
    {prompt: "When I am upset I often act without thinking.", name:'UPPS13', required: true, labels:likert_scale},
    {prompt: "I welcome new and exciting experiences and sensations, even if they are a little frightening and unconventional.", name:'UPPS14', required: true, labels:likert_scale},
    {prompt: "When I feel rejected, I will often say things that I later regret.", name:'UPPS15', required: true, labels:likert_scale},
    {prompt: "I would like to learn to fly an airplane.", name:'UPPS16', required: true, labels:likert_scale},
    {prompt: "Others are shocked or worried about the things I do when I am feeling very excited.", name:'UPPS17', required: true, labels:likert_scale},
    {prompt: "I would enjoy the sensation of skiing very fast down a high mountain slope.", name:'UPPS18', required: true, labels:likert_scale},
    {prompt: "I usually think carefully before doing anything.", name:'UPPS19', required: true, labels:likert_scale},
    {prompt: "I tend to act without thinking when I am really excited.", name:'UPPS20', required: true, labels:likert_scale}
      ],

  on_finish: function(data) {
    jsPsych.data.addProperties({
        UPPS1_lps: JSON.parse(data.responses)['UPPS1'],
        UPPS2_lpm: JSON.parse(data.responses)['UPPS2'],
        UPPS3_pu: JSON.parse(data.responses)['UPPS3'],
        UPPS4_lps: JSON.parse(data.responses)['UPPS4'],
        UPPS5_lpm: JSON.parse(data.responses)['UPPS5'],
        UPPS6_nu: JSON.parse(data.responses)['UPPS6'],
        UPPS7_lps: JSON.parse(data.responses)['UPPS7'],
        UPPS8_nu: JSON.parse(data.responses)['UPPS8'],
        UPPS9_ss: JSON.parse(data.responses)['UPPS9'],
        UPPS10_pu: JSON.parse(data.responses)['UPPS10'],
        UPPS11_lps: JSON.parse(data.responses)['UPPS11'],
        UPPS12_lpm: JSON.parse(data.responses)['UPPS12'],
        UPPS13_nu: JSON.parse(data.responses)['UPPS13'],
        UPPS14_ss: JSON.parse(data.responses)['UPPS14'],
        UPPS15_nu: JSON.parse(data.responses)['UPPS15'],
        UPPS16_ss: JSON.parse(data.responses)['UPPS16'],
        UPPS17_pu: JSON.parse(data.responses)['UPPS17'],
        UPPS18_ss: JSON.parse(data.responses)['UPPS18'],
        UPPS19_lpm: JSON.parse(data.responses)['UPPS19'],
        UPPS20_pu: JSON.parse(data.responses)['UPPS20']
    });
  }
};


// ****************************************************************************
// *                                    Run                                   *
// ****************************************************************************

// Setup Timeline
var start_ls = [fs, PID_ID, start_inst];

var survey_ls = [BISBAS, NFC, BFI, UPPS_P]

var end_ls   = [end_screen]

timeline     = start_ls.concat(survey_ls, end_ls);


// Run jsPsych
jsPsych.init({
  timeline: timeline,
  on_finish: function() {
    jsPsych.data.get().localSave('csv', `${PID}_survey.csv`);
  }
});
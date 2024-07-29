# DACFE: Demand-related Affect and Choice fEMG study
# coding=utf-8

# Rating of Cues and N-back task
# coding=utf-8
# import msilib  # for Microsoft

# continueRoutine defaults to being True. Only need to set to "False" when terminating.


from .constant import *
from .letter_stimuli import *

## Initialize components for Routine "instructions" ##

def show_instruction(inst_dir, data, start_num=0):

    responses = []
    check_esc()

    slides = os.listdir(inst_dir)  # return a list of file(or folder) names
    slides = [slide for slide in slides if slide[0] == 'S']  # 'slide' is a string
    slide_nums = sorted([int(slide[5:-4]) for slide in slides])  # extract num from 'Slide1.png'
    # print('amount of sliders: ', slide_nums)
    total_num = len(slides)
    pic = visual.ImageStim(WIN, image=None)

    ### TRIGGER - INST ###
    this_trig = DF_TRIG[DF_TRIG.TriggerName == 'instructions']['Code'].iloc[0]

    counter = start_num
    while -total_num < counter < total_num:
        response = None
        MS.clickReset()
        pic.image = f'{inst_dir}Slide{slide_nums[counter]}.png'
        pic.draw()
        WIN.flip()
        # send trigger
        sendTrigger(SER, this_trig)

        start_time = GLOBALCLOCK.getTime()

        if IF_SEE_COMPUTR_PLAY:
            core.wait(AI_INSTRUCTION_TIME)
            response = 'right'
        else:
            while True:
                key_press = KB.getKeys(keyList=['escape'])
                buttons, click_time = MS.getPressed(getTime=True)
                # although click_time is not used later, it allows the mouse recording more precise

                if 'escape' in key_press:
                    response = 'escape'
                    event.clearEvents()
                    # print('response:', response)
                    core.quit()
                    break

                if buttons[0] == 1:
                    response = 'left'
                    event.clearEvents()
                    # print('response:', response)
                    counter -= 1
                    # print(counter)
                    core.wait(0.1)
                    break
                elif buttons[2] == 1:
                    response = 'right'
                    event.clearEvents()
                    # print('response:', response)
                    counter += 1
                    # print(counter)
                    core.wait(0.1)
                    break
            core.wait(0.1)

            # print(response)
        # print(response)
        responses.append(response)

        end_time = GLOBALCLOCK.getTime()

        data.addData('Instruction',    counter)
        data.addData('Stimulus',       pic.image)
        data.addData('Key',            response)
        data.addData('RT',             end_time - start_time)
        ### RECORD TIME ###
        data.addData('START',          start_time)
        data.addData('END',            end_time)
        data.nextEntry()

        # print(response)
        # print(responses)

    response = responses[-1]
    # print('last', response)

    return response

## TRIAL ROUTINE ##
# n-Back Trial Routine #
def trial_nBack(thisISI, nLevel, phase, block, trialN, data, reminders: bool, run=RUN):

    if phase in ["practice", "practice_main"]:
        stim_phase = "practice"
    elif phase in ["Learning", "Choice"]:
        stim_phase = "test"
    else:
        stim_phase = phase
    # print(stim_phase)
    # print(thisISI)

    if phase == "Learning":
        sub_phase = "learning"
    elif phase == "Choice":
        sub_phase = "choice"
    else:
        sub_phase = phase

    if phase == "practice":
        stim_dura_limit = 9999  # no time limit
    else:
        stim_dura_limit = .5

    # print('trial_start_global_time_point: ', GLOBALCLOCK.getTime())
    TrialClock = core.Clock()
    MS.clickReset()

    this_letter_num = 0
    letter_same_count = 0
    letter_diff_count = 0
    letter_invalid_count = 0
    letter_resp = None
    letter_rt = None
    is_timeout = None
    # "SAME" is Signal    "DIFFERENT" is Noise
    Hits = 0  # hit response count (click 'Same' when 'Same')
    FAs = 0  # false alarm response count (click 'Same' when 'Different')
    CDs = 0  # correct deny count (click 'Different' when 'Different')
    SMiss = 0  # no response on 'Same' letter
    DMiss = 0  # no response on 'Different' letter
    Miss = SMiss + DMiss  # no response count
    CDR = 0  # correct rate on 'Different' letters (wrongly click 'Same' when 'Different', excluding Miss)
    FAR = 0  # false rate on 'Different' letters (wrongly click 'Same' when 'Different', excluding Miss)
    A = 0
    correct_count = 0
    RTs = []

    #  letterList: what curr_letter is
    llname = f'letters_{nLevel}_back_{stim_phase}_Run_{run}_ISI_{thisISI}_trial_{trialN}'
    letterList = globals()[llname]
    # print('letterList', letterList)

    #  reminders letterList
    letter_1back_List = [' '] + letterList[:-1]
    letter_2back_List = [' ', ' '] + letterList[:-2]
    letter_3back_List = [' ', ' ', ' '] + letterList[:-3]
    # print('1-back', letter_1back_List, 'length = ', len(letter_1back_List))
    # print('2-back', letter_2back_List, 'length = ', len(letter_2back_List))
    # print('3-back', letter_3back_List, 'length = ', len(letter_3back_List))

    #  letter_type: curr_letter is target or not
    ltname = f'letters_type_{nLevel}_back_{stim_phase}_Run_{run}_ISI_{thisISI}_trial_{trialN}'
    iftargetList = globals()[ltname]

    for letter in letterList:

        check_esc()

        # print(this_letter_num)
        letter_1back = letter_1back_List[this_letter_num]
        letter_2back = letter_2back_List[this_letter_num]
        letter_3back = letter_3back_List[this_letter_num]
        is_target = iftargetList[this_letter_num]
        this_letter_num += 1
        # correct response of the target letter
        if is_target == '1':
            letter_trig = DF_TRIG[DF_TRIG.TriggerName == 'letterSame']['Code'].iloc[0]  # Trigg Letter Type
            correct_click = 'left'  # 'SAME'
            letter_same_count += 1
        elif is_target == '0':
            letter_trig = DF_TRIG[DF_TRIG.TriggerName == 'letterDiff']['Code'].iloc[0]  # Trigg Letter Type
            correct_click = 'right'  # 'DIFFERENT'
            letter_diff_count += 1

        curr_letter = visual.TextStim(WIN, text=letter, height=0.08, color='white')

        # present fixation
        FIXATION.draw()
        WIN.flip()
        # trigger start
        this_trig = DF_TRIG[DF_TRIG.TriggerName == 'fixaLetter']['Code'].iloc[0]  # Trigg Fixation
        startTrigger(SER, this_trig)
        core.wait(FIXA_LETTER_DUR)
        # trigger end
        endTrigger(SER)

        # present letter stimulus
        curr_letter.draw()

        # present tips during slow practice
        if phase == "practice" and reminders is True:
            # set the color of target nback letters
            color1 = 'gray'
            color2 = 'gray'
            color3 = 'gray'
            if nLevel == 1:
                color1 = 'yellow'
            elif nLevel == 2:
                color2 = 'yellow'
            elif nLevel == 3:
                color3 = 'yellow'

            curr_1back_letter = visual.TextStim(WIN, text=f'{letter_1back}',
                                                height=0.08, pos=(-0.1, 0), color=color1)
            curr_2back_letter = visual.TextStim(WIN, text=f'{letter_2back}',
                                                height=0.08, pos=(-0.2, 0), color=color2)
            curr_3back_letter = visual.TextStim(WIN, text=f'{letter_3back}',
                                                height=0.08, pos=(-0.3, 0), color=color3)
            resp_tip = visual.TextStim(WIN, text='  Same = Left      Different = Right',
                                       height=0.05, pos=(0, 0.25), color='white')

            # draw tips
            resp_tip.draw()
            curr_1back_letter.draw()
            curr_2back_letter.draw()
            curr_3back_letter.draw()

        WIN.flip()
        # send trigger
        startTrigger(SER, letter_trig)

        start_time = GLOBALCLOCK.getTime()
        # print('letter_start_time: ', start_time)

        # reset click before each letter loop
        MS.clickReset()

        TrialClock.reset()
        while TrialClock.getTime() < (stim_dura_limit + (thisISI / 1000)):
            now_time = GLOBALCLOCK.getTime()
            stim_dura = now_time - start_time

            resp, rt = MS.getPressed(getTime=True)

            if stim_dura >= stim_dura_limit:
                WIN.flip()
                # print('stim_dura:', stim_dura)
                # end trigger
                endTrigger(SER)

            if sum(resp) == 0:
                is_timeout = 1
                is_correct = 0
                letter_rt = np.nan

            else:
                is_timeout = 0
                resp_click = resp.index(1)
                if resp_click == 0:
                    letter_resp = 'left'
                    letter_rt = rt[0]
                    # print('resp:', letter_resp, 'rt:', letter_rt)
                elif resp_click == 2:
                    letter_resp = 'right'
                    letter_rt = rt[2]
                    # print('resp:', letter_resp, 'rt:', letter_rt)
                
                if letter_resp == correct_click:
                    # send trigger
                    this_trig = DF_TRIG[DF_TRIG.TriggerName == 'respLetterCorrect']['Code'].iloc[0]  # Trigg Correct Response
                    sendTrigger(SER, this_trig)
                    is_correct = 1
                    break
                
                else:
                    # send trigger
                    this_trig = DF_TRIG[DF_TRIG.TriggerName == 'respLetterError']['Code'].iloc[0]  # Trigg Correct Response
                    sendTrigger(SER, this_trig)
                    is_correct = 0 
                    break
        core.wait(0.15)
        RTs.append(letter_rt)
        # print('curr_trial_time_point: ', TrialClock.getTime())
        # print('curr_global_time_point: ', GLOBALCLOCK.getTime())

        if is_timeout == 1:
            # send trigger
            this_trig = DF_TRIG[DF_TRIG.TriggerName == 'respLetterTimeout']['Code'].iloc[0]  # Trigg Response Timeout
            sendTrigger(SER, this_trig)
            if phase == 'practice' and reminders is True:
                    feedback_text = 'Too Slow'
                    feedback_color = 'yellow'
                    feedback_prac = visual.TextStim(win=WIN, text=feedback_text,
                                                    height=.05, pos=(0, 0), color=feedback_color)
                    feedback_prac.draw()
                    WIN.flip()
                    core.wait(FEEDBACK_DUR)
            if is_target == '0':
                DMiss += 1
            elif is_target == '1':
                SMiss += 1
            Miss = SMiss + DMiss
            # print('Miss=', Miss)  
            
        else:
            if is_correct == 1:
                if phase == 'practice' and reminders is True:
                    feedback_text = 'Correct'
                    feedback_color = 'green'
                    feedback_prac = visual.TextStim(win=WIN, text=feedback_text,
                                                    height=.05, pos=(0, 0), color=feedback_color)
                    feedback_prac.draw()
                    WIN.flip()
                    core.wait(0.5)
                correct_count += 1
                if is_target == '1':
                    Hits += 1
                elif is_target == '0':
                    CDs += 1   

            else:
                if phase == 'practice' and reminders is True:
                        feedback_text = 'Wrong'
                        feedback_color = 'red'
                        feedback_prac = visual.TextStim(win=WIN, text=feedback_text,
                                                        height=.05, pos=(0, 0), color=feedback_color)
                        feedback_prac.draw()
                        WIN.flip()
                        core.wait(0.5)
                        WIN.flip()
                        core.wait(0.5)
                if is_target == '1':
                    FAs += 1
  

        MS.clickReset()

        ### SAVE DATA for each Letter in one Trial ###
        data.addData('Phase', sub_phase)
        data.addData('Block', block)
        data.addData('TrialN', trialN)
        data.addData('NbackLevel', nLevel)
        data.addData('ISI', thisISI)
        data.addData('LetterN', this_letter_num)
        data.addData('Letter', letter)
        data.addData('Letter_isSame', is_target)
        data.addData('Letter_Resp', letter_resp)
        data.addData('Letter_RT', letter_rt)
        data.addData('Letter_Accuracy', is_correct)
        data.addData('Letter_Timeout', is_timeout)
        data.nextEntry()

    # print('trial_end_global_time_point: ', GLOBALCLOCK.getTime())

    #  calculate A use 'calculate_A' function

    indicators = calculate_A(letter_same_count, letter_diff_count, letter_invalid_count,
                             Hits, FAs, DMiss, Miss, CDs)
    A = indicators[0]
    HR = indicators[1]
    FAR = indicators[2]
    CDR = indicators[3]
    MSR = indicators[4]
    this_trial_acc = 1 - FAR - MSR
    this_trial_rt = np.nanmean(np.array(RTs))  # mean of RTs on letters
    # print(np.array(RTs))

    ### SAVE DATA for each Trial ###
    data.addData('Phase', phase)
    data.addData('Block', block)
    data.addData('TrialN', trialN)
    data.addData('NbackLevel', nLevel)
    data.addData('ISI', thisISI)
    data.addData('Trial_A_measure', A)
    data.addData('Trial_HR', HR)
    data.addData('Trial_FAR', FAR)
    data.addData('Trial_CDR', CDR)
    data.addData('Trial_MSR', MSR)
    data.addData('Trial_ACC', this_trial_acc)
    data.addData('Trial_RT', this_trial_rt)

    data.addData('Trial_HitsCount', Hits)
    data.addData('Trial_FAsCount', FAs)
    data.addData('Trial_SameNoRespCount', SMiss)
    data.addData('Trial_DiffNoRespCount', DMiss)
    data.addData('Trial_NoRespCount', Miss)
    data.addData('Trial_CDsCount', CDs)
    data.addData('Trial_CorrectRespCount', correct_count)

    data.addData('Trial_SameLetterCount', letter_same_count)
    data.addData('Trial_DiffLetterCount', letter_diff_count)
    data.addData('Trial_InvalidLetterCount', letter_invalid_count)

    data.nextEntry()

    return A


### CALCULATE A MEASURE ###
def calculate_A(letter_same_count, letter_diff_count, letter_invalid_count,
                Hits, FAs, DMiss, Miss, CDs):
    if letter_same_count > 0:
        HR = (Hits / letter_same_count)
    else:
        HR = np.nan
        A = np.nan
        letter_invalid_count += 1

    if letter_diff_count > 0:
        FAR = (FAs / letter_diff_count)
        # Todd used DER instead of FAR, to exclude "DiffNoResp" in (1-FAR).
        # But I use FAR, meanwhile, I use CDR instead of (1-FAR), which exclude "DiffNoResp".
        # So FAR + CDR < 1 when DMiss > 0.
        if letter_diff_count != DMiss:
            CDR = (CDs / (letter_diff_count - DMiss))
        else:
            FAR = np.nan
            CDR = np.nan
            A = np.nan
    else:
        FAR = np.nan
        CDR = np.nan
        A = np.nan
        letter_invalid_count += 1

    if (letter_same_count + letter_diff_count) > 0:
        MSR = Miss / (letter_same_count + letter_diff_count)
    else:
        MSR = "NA"
        A = "NA"
        letter_invalid_count += 1

    #  calculate measure A
    if not letter_invalid_count:
        if FAR == HR:
            A = 0.5
        elif FAR <= 0.5 <= HR:  # the left up quadrant of ROC plot above y=x diagonal
            A = 3/4 + ((HR-FAR)/4) - (FAR*(1-HR))
        elif FAR <= HR < 0.5:  # the left down quadrant of ROC plot above y=x diagonal
            if HR == 0:
                HR += 1e-100
            A = 3/4 + ((HR-FAR)/4) - (FAR/(4*HR))  # Error could occur when FAR=HR=0 (DiffResp on all Same trials & Miss on all Diff trials)
        elif 0.5 < FAR <= HR:  # the left up quadrant of ROC plot above y=x diagonal
            if CDR == 0:
                CDR += 1e-100
            A = 3/4 + ((HR-FAR)/4) - ((1-HR)/(4*CDR))  # Error could occur when CDR=0 (no DiffResp on any Diff trials)
        elif HR <= 0.5 <= FAR:  # the right down quadrant of ROC plot below y=x diagonal
            A = 1/4 + ((HR-FAR)/4) - (HR*CDR)
        elif HR <= 0.5 and FAR < 0.5:  # the left down quadrant of ROC plot below y=x diagonal
            if FAR == 0:
                FAR += 1e-100
            A = 1/4 + ((HR-FAR)/4) - (HR/(4*FAR))  # Error could occur when FAR=0 (no FA)
        elif 0.5 < HR <= FAR:  # the right up quadrant of ROC plot below y=x diagonal
            if HR == 1:
                HR -= 1e-100
            A = 1/4 + ((HR-FAR)/4) - (CDR/(4*(1-HR)))  # Error could occur when HR=1=FAR (SameResp on all Same and Diff trials)

    #  limit range of A = [0, 1]
    if A < 0:
        A = 0
    elif A > 1:
        A = 1

    return A, HR, FAR, CDR, MSR

### CHECK A MEASURE ###
def check_A(A, A_min, A_max, ISI, nLevel, reminder):
    event.clearEvents()
    while A < A_min or np.isnan(A):
        show_instruction(f'{INST_PATH}inst_redo_{nLevel}{os.sep}', data=EXPDATA)
        buffer(show="rePrac")
        A = trial_nBack(thisISI=ISI, nLevel=nLevel, phase='practice', block=0,
                        trialN=random.sample(trialNs_prac, 1)[0], reminders=reminder, data=EXPDATA)
        if A >= A_max:
            break



## CALIBRATION ROUTINE ##
def ISI_calibration(curr_ISI_level, data, block=0,):
    trial_count = 0
    trial_count_cali = 0

    while trial_count < TRIAL_NUM_CALI:
        trial_count += 1
        trial_count_cali += 1
        print(trial_count_cali)

        curr_ISI = ISIs[f'{curr_ISI_level}']

        buffer(show="start_seq")
        curr_A = trial_nBack(thisISI=curr_ISI, nLevel=2, phase='calibration', block=0,
                    trialN=random.sample(trialNs_prac, 1)[0], reminders=False, data=data)  # return an A
        A = curr_A
        # feedback_text = f'Performance score: {A*100:.2f}'
        # feedback_cali = visual.TextStim(win=WIN, text=feedback_text, height=.04, pos=(0, 0), color='white')
        # feedback_cali.draw()
        WIN.flip()
        core.wait(1.5)

        data.addData('Phase', "Calibration")
        data.addData('Block', block)
        data.addData('NbackLevel', 2)
        data.addData('ISI', curr_ISI)
        data.addData('TrialCountCali', trial_count_cali)
        data.nextEntry()

        if A < A_min or np.isnan(A):
            if curr_ISI_level > 1:
                curr_ISI_level -= 1  # lower ISI_level = longer ISI
            if trial_count == TRIAL_NUM_CALI:
                trial_count -= 1
        elif A > A_max:
            if curr_ISI_level < len(ISI_levels):
                curr_ISI_level += 1
            # if trial_count == TRIAL_NUM_CALI:
            #     trial_count -= 1
        # print(A)

    ISI_calibrated = curr_ISI

    buffer(show="end")

    data.addData('Phase', "CALIBRATION")
    data.addData('Block', block)
    data.addData('TrialCountCali', trial_count_cali)
    data.addData('CaliEnd_A_measure', A)
    data.addData('ISI_calibrated', ISI_calibrated)
    data.nextEntry()

    return ISI_calibrated



## MAIN TASK BLOCK ROUTINE ##
# phase = ['Practice, 'Learning']
def main_block(phase, testISI, data, block, run=RUN):

    trialTimer = core.Clock()
    total_trial_num = 0
    valid_trial_num = 0

    if phase == 'PRACTICE':
        curr_phase = 'practice_main'
        cond_df_rd = cond_df.sample(frac=1).reset_index()
        num_trials = TRIAL_NUM_PRAC_MAIN  # Only 3 trials in practice
        cue_path = STIM_CUE_PRAC_PATH
    elif phase == 'LEARNING':
        curr_phase = 'Learning'
        cond_df_rd = cond_df[cond_df['block'] == block].reset_index()
        # print('cond_df_select', cond_df['block'] == block_num)
        # print('cond_df_rd', cond_df_rd)
        num_trials = TRIAL_NUM_LEARNING  # 50 trials
        cue_path = STIM_CUE_LEARNING_PATH
    else:
        num_trials = 0
        core.quit()
        print('No phase chosen.')

    while valid_trial_num < num_trials:

        check_esc()

        for this_trial_num in range(valid_trial_num, num_trials):
            total_trial_num += 1
            # print('trial_nums:', range(valid_trial_num, num_trials))
            # print('valid_trial_num:', valid_trial_num)
            # print('this_trial_num:', this_trial_num)

            trial_id = cond_df_rd.loc[valid_trial_num, 'trialID']
            curr_cue = cond_df_rd.loc[valid_trial_num, 'cueLearning']
            curr_trial_demand = cond_df_rd.loc[valid_trial_num, 'trialDemandLearning']
            curr_level = cond_df_rd.loc[valid_trial_num, 'nBackLevelLearning']

            CUE = visual.ImageStim(win=WIN, image=f'{cue_path}{curr_cue}')

            #  trial begin  ##
            # send trigger
            this_trig = DF_TRIG[DF_TRIG.TriggerName == 'trialStart']['Code'].iloc[0]  # Trigg Trial
            sendTrigger(SER, this_trig)

            trialTimer.reset()

            # fixation
            FIXATION.draw()
            WIN.flip()
            # send trigger
            this_trig = DF_TRIG[DF_TRIG.TriggerName == 'fixaCue']['Code'].iloc[0]  # Trigg Fixation
            startTrigger(SER, this_trig)
            core.wait(FIXA_CUE_DUR)
            # end trigger
            endTrigger(SER)

            # set trigger
            this_trig = DF_TRIG[DF_TRIG.TriggerName == f'cue{curr_trial_demand}']['Code'].iloc[0]  # Trigg Cue
            while (trialTimer.getTime()-FIXA_CUE_DUR) < CUE_DUR:
                check_esc()

                CUE.draw()
                cueOnsetTime = GLOBALCLOCK.getTime()
                WIN.flip()
                startTrigger(SER, this_trig)

            # end trigger
            endTrigger(SER)

            # fixation
            FIXATION.draw()
            WIN.flip()
            # send trigger
            this_trig = DF_TRIG[DF_TRIG.TriggerName == 'fixaSeq']['Code'].iloc[0]  # Trigg Fixation
            startTrigger(SER, this_trig)
            core.wait(FIXA_SEQ_DUR)
            # end trigger
            endTrigger(SER)

            begin_text = f'{curr_level}-Back Task\n\nSequence Begin'
            begin_cali = visual.TextStim(win=WIN, text=begin_text, height=.04, pos=(0, 0), color='white')
            begin_cali.draw()
            WIN.flip()
            # send trigger
            this_trig = DF_TRIG[DF_TRIG.TriggerName == f'seqStart_N{curr_level}']['Code'].iloc[0]  # Trigg Trial
            startTrigger(SER, this_trig)
            core.wait(TRIAL_INST_DUR)
            # end trigger
            endTrigger(SER)

            # print('valid_trialN:', valid_trial_num+1)

            trial_nBack(thisISI=testISI, nLevel=curr_level, phase=curr_phase, block=block,
                        trialN=valid_trial_num+1,
                        reminders=False,
                        data=EXPDATA)

            WIN.flip()  # blank

            valid_trial_num += 1

            end_text = 'Sequence End'
            end_seq = visual.TextStim(win=WIN, text=end_text, height=.04, pos=(0, 0), color='white')
            end_seq.draw()
            WIN.flip()
            # send trigger
            this_trig = DF_TRIG[DF_TRIG.TriggerName == 'seqEnd']['Code'].iloc[0]  # Trigg Trial
            sendTrigger(SER, this_trig)

            core.wait(TRIAL_INST_DUR)
            WIN.flip()  # blank
            # send trigger
            this_trig = DF_TRIG[DF_TRIG.TriggerName == 'trialEnd']['Code'].iloc[0]  # Trigg Trial
            sendTrigger(SER, this_trig)

            ### ---------- Save Data of Each Trial ---------- ###
            # EXPDATA.addData('GLOBALTRIAL', GLOBALTRIAL)
            data.addData('Run', run)
            data.addData('Phase', phase)
            data.addData('Block', block)
            data.addData('TrialN', valid_trial_num)
            data.addData('TrialIndex', trial_id)
            data.addData('TrialNumber_total', total_trial_num)
            data.addData('TrialNumber_valid', valid_trial_num)
            data.addData('NbackLevel', curr_level)
            data.addData('ISI', testISI)
            data.addData('CueLearning', curr_cue)
            data.addData('TrialDemandLearning', curr_trial_demand)
            data.addData('CueMapping', cue_map)

            ### TIME STAMP ###
            data.addData('CueSTART', cueOnsetTime)
            data.addData('END', datetime.datetime.now().strftime("%y%m%d_%H%M%S"))
            ### SAVE BEHAVIOR DATA ###
            data.nextEntry()


def demand_choice(testISI, data, phase, type, block=9, run=RUN):
    MS.clickReset()
    check_esc()

    cond_df_rd = cond_df.reset_index()
    cue_path = STIM_CUE_CHOICE_PATH

    trialTimer = core.Clock()
    total_trial_num = 0
    valid_trial_num = 0

    if type == "True":
        start_num = 0
        num_trials = start_num + TRIAL_NUM_CHOICE_TRUE

    else:
        start_num = 10
        num_trials = TRIAL_NUM_CHOICE_FALSE

    while valid_trial_num < num_trials:

        check_esc()

        for this_trial_num in range(valid_trial_num, num_trials):
            total_trial_num += 1
            # print('trial_nums:', range(valid_trial_num, num_trials))
            # print('valid_trial_num:', valid_trial_num)
            # print('this_trial_num:', this_trial_num)

            trial_index = start_num + valid_trial_num
            trial_id = cond_df_rd.loc[trial_index, f'choice{type}ID']
            cue_left = cond_df_rd.loc[trial_index, 'cueLeft']
            cue_demand_left = cond_df_rd.loc[trial_index, 'cueDemandLeft']
            cue_right = cond_df_rd.loc[trial_index, 'cueRight']
            cue_demand_right = cond_df_rd.loc[trial_index, 'cueDemandRight']

            CUE_LEFT = visual.ImageStim(win=WIN, image=f'{cue_path}{cue_left}', pos=(-0.2, -0.05))
            CUE_RIGHT = visual.ImageStim(win=WIN, image=f'{cue_path}{cue_right}', pos=(0.2, -0.05))

            textChoice = visual.TextStim(win=WIN, text=' Please choose the one image you prefer.',
                                         height=.04, pos=(0, 0.2), color='white')

            ##  trial begin  ##
            trialTimer.reset()
            # send trigger
            this_trig = DF_TRIG[DF_TRIG.TriggerName == 'trialStart']['Code'].iloc[0]  # Trigg Trial
            sendTrigger(SER, this_trig)

            # fixation
            FIXATION.draw()
            WIN.flip()
            # send trigger
            this_trig = DF_TRIG[DF_TRIG.TriggerName == 'fixaProbChoice']['Code'].iloc[0]  # Trigg Fixation
            startTrigger(SER, this_trig)
            core.wait(FIXA_CHOICE_DUR)
            # end trigger
            endTrigger(SER)

            # set trigger
            this_trig = DF_TRIG[DF_TRIG.TriggerName == f'probChoice{type}']['Code'].iloc[0]  # Trigg Choice

            while (trialTimer.getTime()-FIXA_CHOICE_DUR) < CHOICE_TIMEOUT:
                check_esc()

                CUE_LEFT.draw()
                CUE_RIGHT.draw()
                cueOnsetTime = GLOBALCLOCK.getTime()

                textChoice.draw()
                choiceOnsetTime = GLOBALCLOCK.getTime()

                WIN.flip()
                startTrigger(SER, this_trig)

                choice = None

                if MS.isPressedIn(CUE_LEFT):
                    # endTrigger(SER)
                    choiceTime = GLOBALCLOCK.getTime()
                    choice = "Left"
                elif MS.isPressedIn(CUE_RIGHT):
                    # endTrigger(SER)
                    choiceTime = GLOBALCLOCK.getTime()
                    choice = "Right"

                if choice is not None:
                    endTrigger(SER)
                    if type == "False":
                        task = "Mid"
                    else:
                        task = choice
                    choice_demand = cond_df_rd.loc[trial_index, f"cueDemand{choice}"]
                    curr_level = int(cond_df_rd.loc[trial_index, f"nBackLevel{task}"])
                    curr_demand = cond_df_rd.loc[trial_index, f"cueDemand{task}"]
                    # send trigger
                    this_trig = DF_TRIG[DF_TRIG.TriggerName == f'respChoice{type}{choice_demand}']['Code'].iloc[0]  # Trigg Choice
                    sendTrigger(SER, this_trig)
                    choice_rt = choiceTime - choiceOnsetTime
                    choice_timeout = 0
                    break
                else:
                    choice_timeout = 1

            # if choice_timeout, choose again
            if choice_timeout == 1:
                # send trigger
                this_trig = DF_TRIG[DF_TRIG.TriggerName == 'respChoiceTimeout']['Code'].iloc[
                    0]  # Trigg Choice
                sendTrigger(SER, this_trig)
                warning_text = 'Please make your choice more quickly!'
                feedbackText = visual.TextStim(win=WIN, text=warning_text, height=.05, pos=(0, 0), color='yellow')
                feedbackText.draw()
                WIN.flip()
                core.wait(1.5)
                # send trigger
                this_trig = DF_TRIG[DF_TRIG.TriggerName == 'trialEnd']['Code'].iloc[0]  # Trigg Trial
                sendTrigger(SER, this_trig)
                WIN.flip()
            else:
                # fixation
                FIXATION.draw()
                WIN.flip()
                # send trigger
                this_trig = DF_TRIG[DF_TRIG.TriggerName == 'fixaSeq']['Code'].iloc[0]  # Trigg Fixation
                startTrigger(SER, this_trig)
                core.wait(FIXA_SEQ_DUR)
                # end trigger
                endTrigger(SER)

                begin_text = f'{curr_level}-Back Task\n\nSequence Begin'
                begin_seq = visual.TextStim(win=WIN, text=begin_text, height=.04, pos=(0, 0), color='white')
                begin_seq.draw()
                WIN.flip()
                # send trigger
                this_trig = DF_TRIG[DF_TRIG.TriggerName == f'seqStart_N{curr_level}']['Code'].iloc[0]  # Trigg Trial
                startTrigger(SER, this_trig)
                core.wait(TRIAL_INST_DUR)
                endTrigger(SER)

                # print('valid_trialN:', valid_trial_num+1)

                trial_nBack(thisISI=testISI, nLevel=curr_level, phase=phase, block=block,
                            trialN=valid_trial_num+1,
                            reminders=False,
                            data=EXPDATA)

                WIN.flip()

                valid_trial_num += 1

                end_text = 'Sequence End'
                end_seq = visual.TextStim(win=WIN, text=end_text, height=.04, pos=(0, 0), color='white')
                end_seq.draw()
                WIN.flip()
                # send trigger
                this_trig = DF_TRIG[DF_TRIG.TriggerName == 'seqEnd']['Code'].iloc[0]  # Trigg Trial
                sendTrigger(SER, this_trig)
                core.wait(TRIAL_INST_DUR)
                # send trigger
                this_trig = DF_TRIG[DF_TRIG.TriggerName == 'trialEnd']['Code'].iloc[0]  # Trigg Trial
                sendTrigger(SER, this_trig)
                WIN.flip()

                ### ---------- Save Data of Each Trial ---------- ###
                # EXPDATA.addData('GLOBALTRIAL', GLOBALTRIAL)
                data.addData('Run', run)
                data.addData('Phase', f"{type}CHOICE")
                data.addData('PhaseType', type)
                data.addData('Block', block)
                data.addData('TrialN', trial_id)
                data.addData('TrialNumber_total', total_trial_num)
                data.addData('TrialNumber_valid', valid_trial_num)
                data.addData('NbackLevel', curr_level)
                data.addData('ISI', testISI)
                data.addData('CueLeft', cue_left)
                data.addData('CueDemandLeft', cue_demand_left)
                data.addData('CueRight', cue_right)
                data.addData('CueDemandRight', cue_demand_right)
                data.addData('CueMapping', cue_map)

                data.addData('Choice', choice)
                data.addData('ChoiceDemand', choice_demand)
                data.addData('TaskDemand', curr_demand)
                data.addData('ChoiceRT', choice_rt)
                data.addData('ChoiceTimeOut', choice_timeout)
                ### TIME STAMP ###
                data.addData('CueSTART', cueOnsetTime)
                data.addData('ChoiceSTART', choiceOnsetTime)
                data.addData('END', datetime.datetime.now().strftime("%y%m%d_%H%M%S"))
                ### SAVE BEHAVIOR DATA ###
                data.nextEntry()



def offline_rating(data, timepoint, run=RUN):
    MS.clickReset()
    check_esc()

    num_trials = TRIAL_NUM_OFFLINE_RATING
    cond_df_rd = cond_df.reset_index()
    cue_path = STIM_CUE_OFFLINE_RATING_PATH

    trialTimer = core.Clock()
    total_trial_num = 0
    valid_trial_num = 0

    while valid_trial_num < num_trials:

        check_esc()

        for this_trial_num in range(num_trials):
            total_trial_num += 1

            trial_id = cond_df_rd.loc[valid_trial_num, 'offlineRatingID']
            curr_cue = cond_df_rd.loc[valid_trial_num, 'offlineRatingCue']
            curr_trial_demand = cond_df_rd.loc[valid_trial_num, 'offlineRatingTrialDemand']
            curr_level = cond_df_rd.loc[valid_trial_num, 'offlineRatingnBackLevel']

            CUE = visual.ImageStim(win=WIN, image=f'{cue_path}{curr_cue}')
            ratingQues = visual.TextStim(win=WIN, text=f'How much do you like this image?',
                                         height=.04, pos=(0, 0.3), color='white')
            ratingScale = visual.Slider(win=WIN,
                                        size=(1.0, 0.08), pos=(0, -0.25),
                                        ticks=[0, 100], startValue=50,
                                        labels=['Not at all', 'Very much'],
                                        granularity=1, style='slider',
                                        lineColor='white', markerColor='red', borderColor='white',
                                        font='Arial', labelWrapWidth=5, labelHeight=0.04)

            ##  trial begin  ##
            # send trigger
            this_trig = DF_TRIG[DF_TRIG.TriggerName == 'trialStart']['Code'].iloc[0]  # Trigg Trial
            sendTrigger(SER, this_trig)

            trialTimer.reset()
            ratingScale.reset()

            # fixation

            FIXATION.draw()
            WIN.flip()
            # send trigger
            this_trig = DF_TRIG[DF_TRIG.TriggerName == 'fixaOfflineRating']['Code'].iloc[0]  # Trigg Fixation
            startTrigger(SER, this_trig)
            core.wait(FIXA_CUE_DUR)
            # end trigger
            endTrigger(SER)

            # set trigger
            this_trig = DF_TRIG[DF_TRIG.TriggerName == f'cue{curr_trial_demand}']['Code'].iloc[0]  # Trigg Cue
            # send trigger
            startTrigger(SER, this_trig)
            while (trialTimer.getTime()-FIXA_CUE_DUR) < CUE_DUR + RATING_TIMEOUT:
                check_esc()
                if (trialTimer.getTime()-FIXA_CUE_DUR) < CUE_DUR:
                    CUE.draw()
                    cueOnsetTime = GLOBALCLOCK.getTime()
                else:
                    # end trigger
                    endTrigger(SER)
                    CUE.draw()
                    ratingScale.draw()
                    ratingQues.draw()
                    ratingOnsetTime = GLOBALCLOCK.getTime()
                    # send trigger
                    this_trig = DF_TRIG[DF_TRIG.TriggerName == f'prob{curr_trial_demand}OfflineRating']['Code'].iloc[0]  # Trigg Rating Scale
                    startTrigger(SER, this_trig)
                WIN.flip()

                if (trialTimer.getTime()-FIXA_CUE_DUR) >= CUE_DUR:
                    ratingScale.getMouseResponses()
                    if ratingScale.getRT() is not None:
                        # end trigger
                        endTrigger(SER)
                        # send trigger
                        this_trig = DF_TRIG[DF_TRIG.TriggerName == f'resp{curr_trial_demand}OfflineRating']['Code'].iloc[0]  # Trigg Rating
                        sendTrigger(SER, this_trig)
                        # print('rating_rt', ratingScale.getRT())
                        rating_rt = ratingScale.getRT()
                        rating_timeout = 0
                        break
                    else:
                        rating_timeout = 1
            # end trigger
            endTrigger(SER)

            # if rating_timeout, rate again
            if rating_timeout == 1:
                # send trigger
                this_trig = DF_TRIG[DF_TRIG.TriggerName == 'respOfflineRatingTimeout']['Code'].iloc[0]  # Trigg Rating
                sendTrigger(SER, this_trig)
                warning_text = 'Please rate more quickly!'
                feedbackText = visual.TextStim(win=WIN, text=warning_text, height=.05, pos=(0, 0), color='yellow')
                feedbackText.draw()
                WIN.flip()
                core.wait(1.5)
                # send trigger
                this_trig = DF_TRIG[DF_TRIG.TriggerName == 'trialEnd']['Code'].iloc[0]  # Trigg Trial
                sendTrigger(SER, this_trig)
            else:
                rating = ratingScale.getMarkerPos()
                valid_trial_num += 1
                # send trigger
                this_trig = DF_TRIG[DF_TRIG.TriggerName == 'trialEnd']['Code'].iloc[0]  # Trigg Trial
                sendTrigger(SER, this_trig)
                WIN.flip()

                MS.clickReset()
                ### ---------- Save Data of Each Question ---------- ###
                data.addData('Run', run)
                data.addData('Phase', "OFFLINERATING")
                data.addData('Block', 9)
                data.addData('OfflineRatingTimePoint', timepoint)
                data.addData('OfflineRatingQuesIndex', trial_id)
                data.addData('CueFigure', curr_cue)
                data.addData('TrialDemand', curr_trial_demand)
                data.addData('NbackLevel', curr_level)
                data.addData('OfflineRating', rating)
                data.addData('OfflineRatingRT', rating_rt)
                data.addData('CueStart', cueOnsetTime)
                data.addData('OfflineRatingStart', ratingOnsetTime)
                data.addData('END', datetime.datetime.now().strftime("%y%m%d_%H%M%S"))
                ### SAVE BEHAVIOR DATA ###
                data.nextEntry()
                break
        buffer(show="blank")



def demand_rating(data, run=RUN):
    MS.clickReset()
    check_esc()
    QuesN = 0
    ratingScale = visual.Slider(win=WIN,
                                size=(1.0, 0.08), pos=(0, -0.15),
                                ticks=[0, 100], startValue=50,
                                labels=['Not at all', 'Very much'],
                                granularity=1, style='slider',
                                lineColor='white', markerColor='red', borderColor='white',
                                font='Arial', labelWrapWidth=5, labelHeight=0.04)

    for dimension, ques in DEMAND_RATING_QUES.items():
        ratingScale.reset()
        TLX = dimension[:-1]
        demand_level = dimension[-1]
        while True:
            check_esc()
            ratingQues = visual.TextStim(win=WIN, text=ques,
                                         height=.04, pos=(0, 0.1), color='white')

            ratingScale.draw()
            ratingQues.draw()
            WIN.flip()
            # send trigger
            this_trig = DF_TRIG[DF_TRIG.TriggerName == f'probTLX_{TLX}_N{demand_level}']['Code'].iloc[0]  # Trigg Rating
            startTrigger(SER, this_trig)
            QuesOnsetTime = GLOBALCLOCK.getTime()
            ratingScale.getMouseResponses()
            if ratingScale.getRT() is not None:
                # end trigger
                endTrigger(SER)
                # send trigger
                this_trig = DF_TRIG[DF_TRIG.TriggerName == f'respTLX_{TLX}_N{demand_level}']['Code'].iloc[0]  # Trigg Rating
                sendTrigger(SER, this_trig)
                QuesN += 1
                rating = ratingScale.getMarkerPos()
                ratingRT = ratingScale.getRT()

                MS.clickReset()
                ### ---------- Save Data of Each Question ---------- ###
                data.addData('Run', run)
                data.addData('Phase', "DEMANDRATING")
                data.addData('Block', 9)
                data.addData('DemandRatingQuesIndex', QuesN)
                data.addData('QuesTLX', TLX)
                data.addData('DemandLevel', demand_level)
                data.addData('DemandRating', rating)
                data.addData('DemandRatingRT', ratingRT)
                data.addData('QuesStart', QuesOnsetTime)
                data.addData('END', datetime.datetime.now().strftime("%y%m%d_%H%M%S"))
                ### SAVE BEHAVIOR DATA ###
                data.nextEntry()
                break
        buffer(show="blank")


def learning_check(data, timepoint, run=RUN):
    MS.clickReset()
    check_esc()

    num_trials = TRIAL_NUM_LEARNING_CHECK
    cond_df_rd = cond_df.reset_index()
    cue_path = STIM_CUE_LEARNING_CHECK_PATH

    trialTimer = core.Clock()
    total_trial_num = 0
    valid_trial_num = 0

    while valid_trial_num < num_trials:

        check_esc()

        for this_trial_num in range(valid_trial_num, num_trials):
            total_trial_num += 1
            # print('trial_nums:', range(valid_trial_num, num_trials))
            # print('valid_trial_num:', valid_trial_num)
            # print('this_trial_num:', this_trial_num)

            trial_id = cond_df_rd.loc[valid_trial_num, 'checkID']
            curr_cue = cond_df_rd.loc[valid_trial_num, 'cueCheck']
            cue_demand = cond_df_rd.loc[valid_trial_num, 'trialDemandCheck']
            if timepoint == "T1":
                mid_text = "Not sure"
                correct_answer = cond_df_rd.loc[valid_trial_num, 'correctAnswer']
            else:
                mid_text = "2-back"
                correct_answer = "Middle"

            CUE = visual.ImageStim(win=WIN, image=f'{cue_path}{curr_cue}')
            RECT_LEFT = visual.Rect(win=WIN, width=0.15, height=0.06,
                                    fillColor="lightgray", pos=(-0.225, -0.25))
            RECT_RIGHT = visual.Rect(win=WIN, width=0.15, height=0.06,
                                    fillColor="lightgray", pos=(0.225, -0.25))
            RECT_MID = visual.Rect(win=WIN, width=0.15, height=0.06,
                                   fillColor="lightgray", pos=(0, -0.25))
            OPTION_LEFT = visual.TextStim(win=WIN, text="1-Back",
                                          height=.03, color="black", pos=(-0.225, -0.25))
            OPTION_RIGHT = visual.TextStim(win=WIN, text="3-Back",
                                           height=.03, color="black", pos=(0.225, -0.25))
            OPTION_MID = visual.TextStim(win=WIN, text=mid_text,
                                         height=.03, color="black", pos=(0, -0.25))

            textCheck = visual.TextStim(win=WIN, text='Which level of letter memory task \n'
                                                      'did this image predict?',
                                         height=.04, pos=(0, 0.3), color='white')

            ##  trial begin  ##
            # send trigger
            this_trig = DF_TRIG[DF_TRIG.TriggerName == 'trialStart']['Code'].iloc[0]  # Trigg Trial
            sendTrigger(SER, this_trig)

            trialTimer.reset()

            # fixation

            FIXATION.draw()
            WIN.flip()
            # send trigger
            this_trig = DF_TRIG[DF_TRIG.TriggerName == 'fixaLearningCheck']['Code'].iloc[0]  # Trigg Fixation
            startTrigger(SER, this_trig)
            core.wait(FIXA_CUE_DUR)
            # end trigger
            endTrigger(SER)

            # send trigger
            this_trig = DF_TRIG[DF_TRIG.TriggerName == 'probLearningCheck']['Code'].iloc[0]  # Trigg Probe
            startTrigger(SER, this_trig)
            while (trialTimer.getTime()-FIXA_CUE_DUR) < 10:

                check_esc()

                CUE.draw()
                RECT_LEFT.draw()
                OPTION_LEFT.draw()
                RECT_RIGHT.draw()
                OPTION_RIGHT.draw()
                RECT_MID.draw()
                OPTION_MID.draw()
                cueOnsetTime = GLOBALCLOCK.getTime()

                textCheck.draw()
                checkOnsetTime = GLOBALCLOCK.getTime()

                WIN.flip()

                answer = None
                if MS.isPressedIn(RECT_LEFT):
                    # end Trigger
                    endTrigger(SER)
                    answerTime = GLOBALCLOCK.getTime()
                    answer = "Left"
                    answer_demand = "Easy"
                elif MS.isPressedIn(RECT_RIGHT):
                    # end Trigger
                    endTrigger(SER)
                    answerTime = GLOBALCLOCK.getTime()
                    answer = "Right"
                    answer_demand = "Hard"
                elif MS.isPressedIn(RECT_MID):
                    # end Trigger
                    endTrigger(SER)
                    answerTime = GLOBALCLOCK.getTime()
                    answer = "Middle"
                    if timepoint == "T1":
                        answer_demand = "unsure"
                    else:
                        answer_demand = "Mid"

                if answer is not None:
                    # send trigger
                    this_trig = DF_TRIG[DF_TRIG.TriggerName == 'respLearningCheck']['Code'].iloc[0]  # Trigg Response
                    sendTrigger(SER, this_trig)
                    answer_rt = answerTime - checkOnsetTime
                    answer_timeout = 0
                    break
                else:
                    answer_timeout = 1

            # if rating_timeout, rate again
            if answer_timeout == 1:
                # send trigger
                this_trig = DF_TRIG[DF_TRIG.TriggerName == 'respChoiceTimeout']['Code'].iloc[0]  # Trigg Choice
                sendTrigger(SER, this_trig)
                warning_text = 'Please indicate your answer more quickly!'
                feedback_cali = visual.TextStim(win=WIN, text=warning_text, height=.05, pos=(0, 0), color='yellow')
                feedback_cali.draw()
                WIN.flip()
                core.wait(2)
                # send trigger
                this_trig = DF_TRIG[DF_TRIG.TriggerName == 'trialEnd']['Code'].iloc[0]  # Trigg Trial
                sendTrigger(SER, this_trig)
            else:
                if answer == correct_answer:
                    answer_acc = 1
                else:
                    answer_acc = 0
                valid_trial_num += 1
                # send trigger
                this_trig = DF_TRIG[DF_TRIG.TriggerName == 'trialEnd']['Code'].iloc[0]  # Trigg Trial
                sendTrigger(SER, this_trig)
                WIN.flip()
                core.wait(2)

                ### ---------- Save Data of Each Trial ---------- ###
                # EXPDATA.addData('GLOBALTRIAL', GLOBALTRIAL)
                data.addData('Run', run)
                data.addData('Phase', "LEARNINGCHECK")
                data.addData('Block', 9)
                data.addData('TrialN', valid_trial_num)
                data.addData('TrialIndex', trial_id)
                data.addData('TrialNumber_total', total_trial_num)
                data.addData('TrialNumber_valid', valid_trial_num)
                data.addData('CueCheck', curr_cue)
                data.addData('CueDemandCheck', cue_demand)
                data.addData('CorrectAnswer', correct_answer)
                data.addData('CueMapping', cue_map)

                data.addData('Answer', answer)
                data.addData('AnswerDemand', answer_demand)
                data.addData('AnswerRT', answer_rt)
                data.addData('AnswerACC', answer_acc)
                data.addData('AnswerTimeOut', answer_timeout)
                ### TIME STAMP ###
                data.addData('CueSTART', cueOnsetTime)
                data.addData('CheckSTART', checkOnsetTime)
                data.addData('END', datetime.datetime.now().strftime("%y%m%d_%H%M%S"))
                ### SAVE BEHAVIOR DATA ###
                data.nextEntry()



def terminal_final_msg():
    ### FINAL MESSAGE TERMINAL ###
    SONA = EXPINFO.get('SONA')
    EXPTR_NAME = EXPINFO.get('EXPERIMENTER').split(' ')[0]
    message = f'------------------------- FINISHED TESTING PARTICIPANT {SONA} ---------------------'
    print(termcolor.colored(message, 'blue'))
    message = f'------------------------- THANK YOU {EXPTR_NAME.upper()} -------------------------'
    print(termcolor.colored(message, 'green'))


def buffer(show):
    if show == "blank":
        buffer_text = ''
        buffer_dura = 1
    elif show == "start":
        buffer_text = 'Start'
        buffer_dura = 0.5
    elif show == "rePrac":
        buffer_text = 'Practice Again'
        buffer_dura = 0.5
    elif show == "start_Test":
        buffer_text = 'Start Test'
        buffer_dura = 1.5
    elif show == "start_seq":
        buffer_text = 'Sequence Begin'
        buffer_dura = 0.5
    elif show == "end_seq":  # between practice trials
        buffer_text = 'Sequence End'
        buffer_dura = 1
    elif show == "end":
        buffer_text = 'End'
        buffer_dura = 0.5
    core.wait(0.5)
    bufferStim = visual.TextStim(win=WIN, text=buffer_text, height=.05, pos=(0, 0), color='white')
    bufferStim.draw()
    WIN.flip()
    core.wait(buffer_dura)


# take 1-minute break between two blocks
def block_break_timer(sec: int):
    countdown_timer = core.CountdownTimer(sec)
    # print('timer', countdown_timer)
    timer_text = visual.TextStim(WIN, text='', color='white', height=0.04, pos=(0, 0))
    while countdown_timer.getTime() > 0:
        timer_text.text = f'Well done! \n\n ' \
                          f'Take a break for 1 minute. \n\n ' \
                          f'Time left: {countdown_timer.getTime():.0f} seconds'
        timer_text.draw()
        WIN.flip()
        check_esc()
        if sum(MS.getPressed()) > 0:
            break
    while sum(MS.getPressed()) == 0:
        timer_text.text = f'Please click the RIGHT button to start next round.'
        timer_text.draw()
        WIN.flip()
        check_esc()
        if MS.getPressed()[1] == 1:
            break


# check for 'Esc' key to quit
def check_esc():
    key_press = KB.getKeys(keyList=['escape'])
    if 'escape' in key_press:
        response = 'escape'
        event.clearEvents()
        print('response is', response)
        core.quit()
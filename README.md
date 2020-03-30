
***

**REDCHECK + DELTA HUB**

***


A **REDCHECK** INTERMEDIACAO E TECNOLOGIA LTDA, pessoa jurídica de direito privado, inscrita no CNPJ/MF sob o nº 33.448.874/0001-65, com sede na Rua Oscar Freire, nº 2040, CEP 05409-011, atua com **Telemedicina e Inteligência Artificial aplicada a imagens médicas**.

Frente a crise provocada pela pandemia relacionada ao Coronavírus, decidimos estabelecer projeto **OpenSource e Colaborativo (sem fins lucrativos)** visando criar inteligências artificiais de suporte a decisão médica em Tomografias Computadorizadas de Tórax e Radiografia de Tórax, para tal estabelecemos parceria com **Delta Hub**, bem como apoio de diversas instituições cujas logotipos se encontram na página do projeto:

[https://covid.redcheck.com.br](https://covid.redcheck.com.br)

Para concretizar a criação dessas ferramentas, pedimos colaboração de todos médicos e clínicas que possam enviar por meio da plataforma imagens relacionadas a casos suspeitos, confirmados, ou descartados de coronavírus.
As imagens são de propriedade daqueles que as enviarem, sendo anonimizadas e mantidas para **acesso somente pelos mesmos**, impedindo que sejam violados princípios que regem a salvaguarda de dados de pacientes, como já é prática da RedCheck.
A RedCheck utiliza plataforma com criptografia de ponta a ponta, e sistemas de backups múltiplos para a segurança dos dados enviados. Todos os usuários cadastrados possuem identidade confirmada, bem como os pacientes.

***

**MODELO DE COLABORAÇÃO:**

***

_Médicos e Clínicas_ – Todos médicos e clínicas devidamente credenciados podem participar enviando imagens na plataforma e se servindo das predições realizadas pelas Inteligências Artificiais, **sem qualquer custo presente ou futuro**.

https://github.com/redcheck-med/covid-dicom/wiki/Critical-use-of-Artificial-Intelligence-tools-(for-doctors)

_Pacientes_ – Como o sistema possui embarcado sistema de envio de laudos por e-mail ou através de Token, os mesmos poderão utilizar da plataforma para acompanhar os laudos de seus exames, caso necessário, sem qualquer custo presente ou futuro.
*Via de regra as imagens são privadas para o médico que as enviou, em caso de interesse de deixa-las públicas, favor preencher este TCLE e assinalar este interesse no campo observações.

https://github.com/redcheck-med/covid-dicom/blob/master/TCLE_RedCheck.docx

_Cientistas e Grupos de Inteligência Artificial e Visão Computacional_ – Devido as características sensíveis e princípios que regem a salvaguarda de dados de pacientes, não poderemos disponibilizar a público o banco de dados, no entanto, **podem ser enviados modelos sugeridos para treino no dataset**, sendo os resultados obtidos prontamente publicados nesta página e enviados para o grupo, juntamente com ranking de desempenho.

_Cientistas e Grupos de Medicina Baseada em Evidências_ – A ferramenta é aberta para médicos enviarem seus exames e checarem o desempenho de classificação das Inteligências Artificiais (IAs), além do mais, o próprio modelo das IAs será disponibilizado nesta página para que possa ser implementado e testado em outras plataformas. É de **fundamental importância a validação externa dos resultados por grupos de pesquisa**, ficamos a disposição para quaisquer esclarecimentos.

Link com orientações para Pesquisadores:

https://github.com/redcheck-med/covid-dicom/wiki/Evidence-Based-Medicine-Considerations-(For-researchers)

https://github.com/redcheck-med/covid-dicom/wiki/List-of-Research-Papers


***

**O MODELO ATUAL DE INTELIGÊNCIA ARTIFICIAL:**

***

**VGG16 + CAM**. O modelo proposto consiste nos _layers_ de convolução de uma VGG16 treinada para o conjunto de dados _imagenet_.

![](https://i.ibb.co/sQ45cX8/Captura-de-tela-2020-03-22-08-26-39.jpg) 


Para treinamento da rede com pouca quantidade de dados congelamos os quatro primeiros blocos de convolução + _pooling_ e retreinamos apenas o ultimo layer:

![](https://i.ibb.co/0hWrmnh/Captura-de-tela-2020-03-22-08-27-12.jpg)



No output do ultimo bloco de convolução aplicamos o _Global Pooling_, que facilita a interpretação das informações aprendidas pelas redes e diminui a necessidade de regularização. Em contraste com as arquiteturas tradicionais temos um modelo mais simples, interpretável e com menor custo computacional. Em conjunto com as _features_ já aprendidas pela VGG16 temos em mãos um modelo robusto e interpretável.


![](https://i.ibb.co/vxjpp2Z/Captura-de-tela-2020-03-22-08-29-05.jpg)


Após a aplicação do _Global Average Pooling_ passamos o output para uma função _Softmax_ e geramos o resultado da classificação.

 
![](https://i.ibb.co/Pc3MMp9/Captura-de-tela-2020-03-22-08-29-56.jpg)


A grande vantagem dessa arquitetura é a possibilidade geração do CAM (_Classification Activation Map_) que torna visíveis as informações aprendidas pelo modelo. Isso nos ajuda a eliminar o problema da “Caixa preta” e nos permite além de realizar a classificação nos mostrar as regiões das imagens que foram relevantes para a tomada de decisão da rede. Essa rede quando bem treinada pode ser uma ferramenta relevante principalmente para funções que envolvam análise de padrões visuais em imagens.

**Parâmetros gerais do modelo:**

Abaixo seguem os parâmetros utilizados para treino desse modelo.

_Learning rate_: 0.01

_Activation_: Softmax

_Otimizador_: SGD

_Input_shape_: (170,256,3)

_Output_shape_: 2

_Classes_: Coronavírus não suspeito e Coronavírus Suspeito

_Loss function_: binary_crossentropy.


**Informações de treino:**

_Aguardando geração dos dados._


**Informações de performance do modelo:**

_Aguardando geração dos dados._


**Demais considerações:**

O modelo acima é uma proposta inicial para desenvolver uma solução que auxilie os profissionais da saúde a fazer a detecção de padrões em exames de imagem da infecção pelo Coronavírus de forma rápida e fácil. Estamos disponíveis para incluir novas implementações e ideias para melhorar a performance do modelo.


***
**Vantagens do Projeto:**
***
**Por serem disponibilizados os Modelos .h5 para testes e uso em outras plataformas e ferramentas, além do código relacionado ao uso de DICOM em plataforma web, o projeto pode ser melhorado e auditado por quaisquer interessados a qualquer momento. Os dados dos pacientes são resguardados e não são acessíveis a público. Os dados tem credibilidade pois são enviados por médicos com registro e têm identificação por CPF do paciente (pacientes reais e médicos reais). Os dados são de origem da linha de cuidado onde pretende-se aplicar a ferramenta. Pela acessibilidade da plataforma e dos modelos de IA, as mesmas podem ter validação externa a qualquer momento por qualquer grupo de pesquisa. Por ser colaborativo, qualquer grupo pode otimizar a IA e nos encaminhar para melhorias na ferramenta. Por fim, como são dados com identificação de origem geográfica, podemos acompanhar as características regionais da pandemia e o comportamento da ferramenta em cada uma dessas regiões.
Os resultados sorológicos são de alto custo, baixa disponibilidade no momento, e atraso significativo na sua disponibilização. Portanto, utilizar de meios de diagnóstico de imagem para presunção diagnóstica, extratificação de risco e diagnóstico diferencial é vital. Como a demanda atual destes exames é alta, criar ferramenta e suporte ao diagnóstico médico de imagem é nossa proposta. Os exames de tomografia apresentam maior acurácia entre especialistas, no entanto, devido não serem amplamente acessíveis, faz-se necessária adotar estratégia paralela com radiografias de tórax, motivo pelo qual ambos os exames foram incluídos.**

***

**Dados para contato:**

***

julio.c.p.rocha@gmail.com Engenheiro de ML Redcheck.

OU

rafael@redcheck.com.br Médico - CEO RedCheck

Os Termos de Uso de Serviços da Plataforma encontram-se disponíveis na tela de cadastro em:
https://covid.redcheck.com.br/account/cadastrar





***

_**English version:**_

***


***

GENERAL PROJECT DATA:

***


REDCHECK INTERMEDIACAO E TECNOLOGIA LTDA, a private legal entity, registered with CNPJ / MF under nº 33.448.874 / 0001-65, headquartered at Rua Oscar Freire, nº 2040, CEP 05409-011 - SP - Brazil, operates with Telemedicine and Artificial Intelligence applied to medical images.
In the face of the crisis caused by the Coronavirus-related pandemic, we decided to establish an OpenSource and Collaborative project (non-profit) aiming to create artificial intelligence to support medical decision-making in CT scans of the chest and chest radiography, for this we established a partnership with Delta Hub, as well as support from several institutions whose logos are on the project page:

https://covid.redcheck.com.br

To concretize the creation of these tools, we ask for the collaboration of all doctors and clinics that can send images related to suspected, confirmed, or discarded coronavirus cases through the platform.
The images are the property of those who send them, is anonymized, and kept for access only by them, preventing the principles governing the safeguarding of patient data from being violated, as is already RedCheck's practice.
RedCheck uses a platform with end-to-end encryption, and multiple backup systems for the security of the data sent. All registered users have a confirmed identity, as well as patients.



***

COLLABORATION MODEL:

***


Doctors and Clinics - All duly accredited doctors and clinics can participate by sending images on the platform and using the predictions made by Artificial Intelligence, without any present or future cost.

https://github.com/redcheck-med/covid-dicom/wiki/Critical-use-of-Artificial-Intelligence-tools-(for-doctors)

Patients - As the system has an embedded system for sending reports by e-mail or through Token, they can use the platform to monitor the descriptions of their exams, if necessary, without any present or future cost.
* As a rule, images are private to the doctor who sent them, in case you are interested in making them public, please fill out this document and indicate this interest in the observations field.

https://github.com/redcheck-med/covid-dicom/blob/master/TCLE_RedCheck.docx

Scientists and Artificial Intelligence and Computer Vision Groups - Due to the sensitive characteristics and principles that govern the safeguarding of patient data, we will not be able to make the database available to the public, however, suggested models can be sent for training in the dataset, being the results obtained promptly published on this page and sent to the group, along with performance ranking.
Scientists and Evidence-Based Medicine Groups - The tools are open for doctors to send their exams and check the Artificial Intelligence (AI) classification performance, in addition, the AI model itself will be made available on this page so that it can be implemented and tested on other platforms. It is of fundamental importance to the external validation of the results by research groups; we are available for any clarifications.

Recommendations link (for researchers):

https://github.com/redcheck-med/covid-dicom/wiki/Evidence-Based-Medicine-Considerations-(For-researchers)

https://github.com/redcheck-med/covid-dicom/wiki/List-of-Research-Papers

***

THE CURRENT MODEL OF ARTIFICIAL INTELLIGENCE:

***


VGG16 + CAM. The proposed model consists of the convolution layers of a VGG16 trained for the imagenet data set.
 
For training the network with a small amount of data, we freeze the first four convolution + pooling blocks and retrain only the last layer:

 

In the output of the last convolution block, we apply Global Pooling, which facilitates the interpretation of information learned by networks and reduces the need for regularization. In contrast to traditional architectures, we have a simpler model, interpretable, and with a lower computational cost. Together with the features already learned by VGG16 we have a robust and interpretable model.
 
After applying Global Average Pooling, we pass the output to a Softmax function and generate the classification result.

 

The great advantage of this architecture is the possibility of generating the CAM (Classification Activation Map) that makes visible the information learned by the model. This helps us to eliminate the "Black Box" problem and allows us, in addition to performing the classification, to show us the regions of the images that were relevant to the network's decision making. This network, when well trained, can be an appropriate tool mainly for functions that involve analysis of visual patterns in images.

General parameters of the model:
Below are the metrics used to train this model. Learning rate: 0.01 Activation: Softmax Optimizer: SGD Input_shape: (170,256.3) Output_shape: 2 Classes: non-suspected Coronavirus and Suspected Coronavirus Loss function: binary_crossentropy.

Training information:
Awaiting data generation.

Model performance information:
Awaiting data generation.

Other considerations:
The model above is an initial proposal to develop a solution that helps healthcare professionals to detect patterns in imaging tests for Coronavirus infection quickly and easily. We are available to include new implementations and ideas to improve the model's performance.

***
** Project Advantages: **
***
**Because the .h5 Models are available for testing and use on other platforms and tools, in addition to the code related to the use of DICOM on the web platform, the project can be improved and audited by any interested party at any time. Patient data is protected and is not accessible to the public. The data is credible because they are sent by registered doctors and have the patient's CPF identification (real patients and real doctors). The data comes from the line of care where the tool is intended to be applied. Due to the accessibility of the platform and the AI ​​models, they can have external validation at any time by any research group. For being collaborative, any group can optimize AI and direct us to improvements in the tool. Finally, as they are data with identification of geographical origin, we can follow the regional characteristics of the pandemic and the behavior of the tool in each of these regions.
Serological results are of high cost, low availability at the moment, and significant delay in their availability. Therefore, using diagnostic imaging tools for diagnostic presumption, risk stratification and differential diagnosis is vital. As the current demand for these exams is high, creating a tool and support for medical imaging diagnosis is our proposal. CT scans are more accurate among specialists, however, because they are not widely accessible, it is necessary to adopt a parallel strategy with chest X-rays, which is why both tests were included.**

***

Contact details:

***

julio.c.p.rocha@gmail.com ML RedCheck engineer.
OR
rafael@redcheck.com.br Physician - CEO RedCheck

The Platform Service Terms of Use are available on the registration screen at:
https://covid.redcheck.com.br/account/cadastrar
